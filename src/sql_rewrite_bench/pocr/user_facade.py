"""Thin user-facing facade for diagnostic POCR support output.

This module adapts existing POCR diagnostic rows into user-output-style files
when a caller supplies an output root. It does not call live APIs, run baseline
adapters, execute SQL, compute official POCR, aggregate route-level POCR, or
promote paper metrics.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sql_rewrite_bench.pocr.annotation_schema import (
    CandidateAnnotation,
    validate_candidate_annotation,
)
from sql_rewrite_bench.pocr.annotation_resolver import ResolvedAnnotationArtifact, resolve_annotation_artifacts
from sql_rewrite_bench.pocr.candidate_resolver import CandidateSource, resolve_candidate_sources
from sql_rewrite_bench.pocr.diagnostic_output_schema import (
    POCRDiagnosticPoolSummary,
    POCRDiagnosticRow,
    summarize_by_pool,
)
from sql_rewrite_bench.pocr.models import SkillContract
from sql_rewrite_bench.pocr.operation_evidence_policy import validate_transformation_stage_b
from sql_rewrite_bench.pocr.skills_parser import parse_skills_file
from sql_rewrite_bench.pocr.user_output_adapter import POCRDiagnosticOutputPaths, write_pocr_diagnostic_user_outputs


@dataclass(frozen=True)
class POCRDiagnosticFacadeResult:
    rows: tuple[POCRDiagnosticRow, ...]
    summaries: tuple[POCRDiagnosticPoolSummary, ...]
    output_paths: POCRDiagnosticOutputPaths | None


def run_pocr_diagnostic_user_facade(
    *,
    repo_root: Path,
    run_id: str,
    candidate_root: Path,
    method_id: str,
    route_id: str,
    engine: str,
    annotation_jsonl: Path | None = None,
    live_enabled: bool = False,
    output_root: Path | None = None,
    case_ids: tuple[str, ...] | None = None,
) -> POCRDiagnosticFacadeResult:
    """Build diagnostic POCR rows and optionally write user-output-style files.

    The facade is deliberately offline by default. When ``live_enabled`` is
    false and no ``annotation_jsonl`` is supplied, it emits rows with
    ``annotation_status=annotation_missing``. The live path remains separately
    gated and is not implemented here.
    """

    if live_enabled:
        raise RuntimeError("live POCR annotation is not enabled in this diagnostic output facade scaffold")
    if not run_id.strip():
        raise ValueError("run_id is required")

    repo_root = repo_root.resolve()
    sources = resolve_candidate_sources(
        repo_root,
        candidate_root=candidate_root,
        method_id=method_id,
        route_id=route_id,
        engine=engine,
        case_ids=case_ids,
    )
    annotations = _resolve_annotations_by_case(
        repo_root,
        annotation_jsonl=annotation_jsonl,
        method_id=method_id,
        route_id=route_id,
        engine=engine,
        case_ids=tuple(source.case_id for source in sources),
    )
    rows = tuple(_row_from_source(repo_root, run_id, source, annotations.get(source.case_id)) for source in sources)
    summaries = summarize_by_pool(rows)
    output_paths = None
    if output_root is not None:
        output_paths = write_pocr_diagnostic_user_outputs(
            output_root=output_root,
            run_id=run_id,
            rows=rows,
            summaries=summaries,
            repo_root=repo_root,
        )
    return POCRDiagnosticFacadeResult(rows=rows, summaries=summaries, output_paths=output_paths)


def _row_from_source(
    repo_root: Path,
    run_id: str,
    source: CandidateSource,
    annotation_artifact: ResolvedAnnotationArtifact | None,
) -> POCRDiagnosticRow:
    parse_result = parse_skills_file(
        repo_root / source.skills_md_path,
        expected_case_id=source.case_id,
        expected_pool=source.pool,
    )
    contract = parse_result.contract
    if contract is None or not parse_result.ok:
        return _empty_row(
            run_id,
            source,
            skill_present=False,
            annotation_status="skill_contract_invalid",
            stage_b_status="missing_skill_contract",
            expected_operation_atoms_count=0,
            semantic_guard_atoms_count=0,
            boundary_notes="skills.md contract missing or invalid; diagnostic row only; no POCR numerator",
        )

    if not source.candidate_present:
        return _empty_row(
            run_id,
            source,
            skill_present=True,
            annotation_status="candidate_missing",
            stage_b_status="missing_candidate",
            expected_operation_atoms_count=len(contract.operation_atoms),
            semantic_guard_atoms_count=len(contract.semantic_guard_atoms),
            boundary_notes="candidate SQL missing; diagnostic row only; no POCR numerator",
        )

    if annotation_artifact is None or annotation_artifact.annotation_status == "missing":
        return _empty_row(
            run_id,
            source,
            skill_present=True,
            annotation_status="annotation_missing",
            stage_b_status="annotation_missing",
            expected_operation_atoms_count=len(contract.operation_atoms),
            semantic_guard_atoms_count=len(contract.semantic_guard_atoms),
            boundary_notes="no Stage A annotation supplied; diagnostic-only POCR facade row",
        )

    if annotation_artifact.annotation_status != "present" or annotation_artifact.annotation is None:
        return _schema_invalid_row(
            run_id,
            source,
            contract,
            boundary_notes=(
                "annotation JSONL replay failed closed: "
                f"status={annotation_artifact.annotation_status}; "
                f"issues={';'.join(annotation_artifact.issue_codes) or 'none'}; "
                f"{annotation_artifact.boundary_notes}"
            ),
        )

    annotation = annotation_artifact.annotation

    schema_issues = validate_candidate_annotation(
        annotation,
        contract,
        expected_engine=source.engine,
        expected_method_id=source.method_id,
        expected_route_id=source.route_id,
    )
    if any(issue.severity == "error" for issue in schema_issues):
        return _schema_invalid_row(
            run_id,
            source,
            contract,
            boundary_notes="annotation failed strict schema or route/case validation; no POCR numerator",
        )

    return _stage_b_row(repo_root, run_id, source, contract, annotation)


def _resolve_annotations_by_case(
    repo_root: Path,
    *,
    annotation_jsonl: Path | None,
    method_id: str,
    route_id: str,
    engine: str,
    case_ids: tuple[str, ...],
) -> dict[str, ResolvedAnnotationArtifact]:
    if annotation_jsonl is None:
        return {}
    rows = resolve_annotation_artifacts(
        repo_root,
        annotation_jsonl=annotation_jsonl,
        method_id=method_id,
        route_id=route_id,
        engine=engine,
        case_ids=case_ids,
    )
    return {row.case_id: row for row in rows}


def _stage_b_row(
    repo_root: Path,
    run_id: str,
    source: CandidateSource,
    contract: SkillContract,
    annotation: CandidateAnnotation,
) -> POCRDiagnosticRow:
    source_sql = (repo_root / source.source_sql_path).read_text(encoding="utf-8-sig")
    candidate_sql = (repo_root / source.candidate_path).read_text(encoding="utf-8-sig")
    positive_sql = (
        (repo_root / source.positive_sql_path).read_text(encoding="utf-8-sig")
        if source.positive_sql_path
        else None
    )
    stage_b = validate_transformation_stage_b(
        contract,
        annotation,
        source_sql=source_sql,
        candidate_sql=candidate_sql,
        positive_sql=positive_sql,
    )
    operation_atoms = [atom for atom in annotation.atoms if atom.atom_type == "operation_atom"]
    return POCRDiagnosticRow(
        run_id=run_id,
        case_id=source.case_id,
        pool=source.pool,
        engine=source.engine,
        method_id=source.method_id,
        route_id=source.route_id,
        candidate_path=source.candidate_path.as_posix(),
        candidate_present=source.candidate_present,
        skill_present=True,
        annotation_status="schema_valid",
        stage_b_status=stage_b.stage_b_status,
        expected_operation_atoms_count=len(contract.operation_atoms),
        stage_a_implemented_operation_atoms_count=sum(
            1 for atom in operation_atoms if atom.observed_status == "implemented"
        ),
        transformation_supported_operation_atoms_count=stage_b.transformation_supported_operation_atoms_count,
        presence_only_operation_atoms_count=stage_b.presence_only_operation_atoms_count,
        insufficient_transformation_evidence_operation_atoms_count=(
            stage_b.insufficient_transformation_evidence_operation_atoms_count
        ),
        rejected_noop_equivalent_operation_atoms_count=stage_b.rejected_noop_equivalent_operation_atoms_count,
        schema_invalid_atoms_count=stage_b.schema_invalid_atoms_count,
        semantic_guard_atoms_count=len(contract.semantic_guard_atoms),
        diagnostic_only=True,
        official_pocr_computed=False,
        route_level_pocr_aggregated=False,
        paper_metric_promoted=False,
        boundary_notes="Stage B transformation-aware validation is diagnostic only; no route-level POCR emitted",
    )


def _empty_row(
    run_id: str,
    source: CandidateSource,
    *,
    skill_present: bool,
    annotation_status: str,
    stage_b_status: str,
    expected_operation_atoms_count: int,
    semantic_guard_atoms_count: int,
    boundary_notes: str,
) -> POCRDiagnosticRow:
    return POCRDiagnosticRow(
        run_id=run_id,
        case_id=source.case_id,
        pool=source.pool,
        engine=source.engine,
        method_id=source.method_id,
        route_id=source.route_id,
        candidate_path=source.candidate_path.as_posix(),
        candidate_present=source.candidate_present,
        skill_present=skill_present,
        annotation_status=annotation_status,
        stage_b_status=stage_b_status,
        expected_operation_atoms_count=expected_operation_atoms_count,
        stage_a_implemented_operation_atoms_count=0,
        transformation_supported_operation_atoms_count=0,
        presence_only_operation_atoms_count=0,
        insufficient_transformation_evidence_operation_atoms_count=0,
        rejected_noop_equivalent_operation_atoms_count=0,
        schema_invalid_atoms_count=0,
        semantic_guard_atoms_count=semantic_guard_atoms_count,
        diagnostic_only=True,
        official_pocr_computed=False,
        route_level_pocr_aggregated=False,
        paper_metric_promoted=False,
        boundary_notes=boundary_notes,
    )


def _schema_invalid_row(
    run_id: str,
    source: CandidateSource,
    contract: SkillContract,
    *,
    boundary_notes: str,
) -> POCRDiagnosticRow:
    return POCRDiagnosticRow(
        run_id=run_id,
        case_id=source.case_id,
        pool=source.pool,
        engine=source.engine,
        method_id=source.method_id,
        route_id=source.route_id,
        candidate_path=source.candidate_path.as_posix(),
        candidate_present=source.candidate_present,
        skill_present=True,
        annotation_status="schema_invalid",
        stage_b_status="schema_invalid",
        expected_operation_atoms_count=len(contract.operation_atoms),
        stage_a_implemented_operation_atoms_count=0,
        transformation_supported_operation_atoms_count=0,
        presence_only_operation_atoms_count=0,
        insufficient_transformation_evidence_operation_atoms_count=0,
        rejected_noop_equivalent_operation_atoms_count=0,
        schema_invalid_atoms_count=len(contract.operation_atoms),
        semantic_guard_atoms_count=len(contract.semantic_guard_atoms),
        diagnostic_only=True,
        official_pocr_computed=False,
        route_level_pocr_aggregated=False,
        paper_metric_promoted=False,
        boundary_notes=boundary_notes,
    )
