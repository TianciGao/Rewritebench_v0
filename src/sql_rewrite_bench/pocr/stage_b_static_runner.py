"""Bounded diagnostic runner for static Stage B POCR evidence validation."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from sql_rewrite_bench.pocr.annotation_resolver import (
    ResolvedAnnotationArtifact,
    resolve_annotation_artifacts,
)
from sql_rewrite_bench.pocr.candidate_resolver import CandidateSource, resolve_candidate_sources
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory
from sql_rewrite_bench.pocr.models import SkillContract
from sql_rewrite_bench.pocr.static_evidence import validate_static_stage_b


@dataclass(frozen=True)
class StaticStageBDiagnosticRow:
    case_id: str
    pool: str
    engine: str
    method_id: str
    route_id: str
    candidate_present: bool
    skill_present: bool
    annotation_present: bool
    annotation_status: str
    stage_b_status: str
    expected_operation_atoms_count: int
    expected_semantic_guard_atoms_count: int
    static_validated_operation_atoms_count: int
    static_rejected_operation_atoms_count: int
    official_pocr_computed: bool
    diagnostic_only: bool
    boundary_notes: str


def build_static_stage_b_diagnostic_rows(
    repo_root: Path,
    *,
    candidate_root: Path,
    method_id: str,
    route_id: str,
    engine: str = "postgres",
    annotation_jsonl: Path | None = None,
    case_ids: tuple[str, ...] | None = None,
) -> tuple[StaticStageBDiagnosticRow, ...]:
    """Combine candidates, skills.md, annotations, and static evidence checks."""

    inventory = build_common_core_inventory(repo_root)
    contract_by_case: dict[str, SkillContract] = {
        member.case_id: result.contract
        for member, result in zip(inventory.members, inventory.parse_results, strict=True)
        if result.contract is not None
    }
    candidates = resolve_candidate_sources(
        repo_root,
        candidate_root=candidate_root,
        method_id=method_id,
        route_id=route_id,
        engine=engine,
        case_ids=case_ids,
    )
    annotations = {
        row.case_id: row
        for row in resolve_annotation_artifacts(
            repo_root,
            annotation_jsonl=annotation_jsonl,
            method_id=method_id,
            route_id=route_id,
            engine=engine,
            case_ids=case_ids,
        )
    }

    rows: list[StaticStageBDiagnosticRow] = []
    for candidate in candidates:
        contract = contract_by_case.get(candidate.case_id)
        annotation = annotations.get(candidate.case_id)
        rows.append(_build_row(repo_root, candidate, contract, annotation))
    return tuple(rows)


def write_static_stage_b_diagnostic_csv(path: Path, rows: tuple[StaticStageBDiagnosticRow, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=static_stage_b_diagnostic_fields(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(static_stage_b_diagnostic_to_csv_rows(rows))


def static_stage_b_diagnostic_to_csv_rows(rows: tuple[StaticStageBDiagnosticRow, ...]) -> list[dict[str, object]]:
    return [
        {
            "case_id": row.case_id,
            "pool": row.pool,
            "engine": row.engine,
            "method_id": row.method_id,
            "route_id": row.route_id,
            "candidate_present": str(row.candidate_present).lower(),
            "skill_present": str(row.skill_present).lower(),
            "annotation_present": str(row.annotation_present).lower(),
            "annotation_status": row.annotation_status,
            "stage_b_status": row.stage_b_status,
            "expected_operation_atoms_count": row.expected_operation_atoms_count,
            "expected_semantic_guard_atoms_count": row.expected_semantic_guard_atoms_count,
            "static_validated_operation_atoms_count": row.static_validated_operation_atoms_count,
            "static_rejected_operation_atoms_count": row.static_rejected_operation_atoms_count,
            "official_pocr_computed": str(row.official_pocr_computed).lower(),
            "diagnostic_only": str(row.diagnostic_only).lower(),
            "boundary_notes": row.boundary_notes,
        }
        for row in rows
    ]


def static_stage_b_diagnostic_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "engine",
        "method_id",
        "route_id",
        "candidate_present",
        "skill_present",
        "annotation_present",
        "annotation_status",
        "stage_b_status",
        "expected_operation_atoms_count",
        "expected_semantic_guard_atoms_count",
        "static_validated_operation_atoms_count",
        "static_rejected_operation_atoms_count",
        "official_pocr_computed",
        "diagnostic_only",
        "boundary_notes",
    ]


def _build_row(
    repo_root: Path,
    candidate: CandidateSource,
    contract: SkillContract | None,
    annotation_artifact: ResolvedAnnotationArtifact | None,
) -> StaticStageBDiagnosticRow:
    skill_present = contract is not None and bool(contract.atoms)
    expected_operation_atoms_count = len(contract.operation_atoms) if contract else 0
    expected_semantic_guard_atoms_count = len(contract.semantic_guard_atoms) if contract else 0
    annotation_status = annotation_artifact.annotation_status if annotation_artifact else "missing"
    annotation_present = annotation_artifact is not None and annotation_artifact.annotation is not None

    if not skill_present:
        return _row(candidate, False, False, annotation_status, "missing_skill_contract", 0, 0, "skills.md missing")
    if not candidate.candidate_present:
        return _row(
            candidate,
            True,
            annotation_present,
            annotation_status,
            "missing_candidate",
            expected_operation_atoms_count,
            expected_semantic_guard_atoms_count,
            "candidate SQL missing; no static evidence validation",
        )
    if annotation_artifact is None or annotation_artifact.annotation is None:
        stage_status = _stage_status_for_unusable_annotation(annotation_status)
        return _row(
            candidate,
            True,
            False,
            annotation_status,
            stage_status,
            expected_operation_atoms_count,
            expected_semantic_guard_atoms_count,
            "no usable Stage A annotation; static Stage B remains fail-closed",
        )

    static_result = validate_static_stage_b(
        contract,
        annotation_artifact.annotation,
        source_sql=(repo_root / candidate.source_sql_path).read_text(encoding="utf-8-sig"),
        candidate_sql=(repo_root / candidate.candidate_path).read_text(encoding="utf-8-sig"),
        positive_sql=_read_optional(repo_root, candidate.positive_sql_path),
    )
    return StaticStageBDiagnosticRow(
        case_id=candidate.case_id,
        pool=candidate.pool,
        engine=candidate.engine,
        method_id=candidate.method_id,
        route_id=candidate.route_id,
        candidate_present=candidate.candidate_present,
        skill_present=True,
        annotation_present=True,
        annotation_status=annotation_status,
        stage_b_status=static_result.stage_b_status,
        expected_operation_atoms_count=expected_operation_atoms_count,
        expected_semantic_guard_atoms_count=expected_semantic_guard_atoms_count,
        static_validated_operation_atoms_count=static_result.static_validated_operation_atoms_count,
        static_rejected_operation_atoms_count=static_result.static_rejected_operation_atoms_count,
        official_pocr_computed=False,
        diagnostic_only=True,
        boundary_notes=(
            "validated_static_span is diagnostic support only; no official POCR or route aggregation"
        ),
    )


def _row(
    candidate: CandidateSource,
    skill_present: bool,
    annotation_present: bool,
    annotation_status: str,
    stage_b_status: str,
    expected_operation_atoms_count: int,
    expected_semantic_guard_atoms_count: int,
    boundary_notes: str,
) -> StaticStageBDiagnosticRow:
    return StaticStageBDiagnosticRow(
        case_id=candidate.case_id,
        pool=candidate.pool,
        engine=candidate.engine,
        method_id=candidate.method_id,
        route_id=candidate.route_id,
        candidate_present=candidate.candidate_present,
        skill_present=skill_present,
        annotation_present=annotation_present,
        annotation_status=annotation_status,
        stage_b_status=stage_b_status,
        expected_operation_atoms_count=expected_operation_atoms_count,
        expected_semantic_guard_atoms_count=expected_semantic_guard_atoms_count,
        static_validated_operation_atoms_count=0,
        static_rejected_operation_atoms_count=0,
        official_pocr_computed=False,
        diagnostic_only=True,
        boundary_notes=boundary_notes,
    )


def _read_optional(repo_root: Path, path: Path | None) -> str | None:
    if path is None:
        return None
    full_path = repo_root / path
    if not full_path.is_file():
        return None
    return full_path.read_text(encoding="utf-8-sig")


def _stage_status_for_unusable_annotation(annotation_status: str) -> str:
    if annotation_status == "missing":
        return "annotation_missing"
    if annotation_status in {"malformed_json", "schema_invalid", "case_mismatch", "route_mismatch"}:
        return "schema_invalid"
    return annotation_status
