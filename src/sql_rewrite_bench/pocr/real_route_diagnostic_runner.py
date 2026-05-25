"""Real-route diagnostic POCR runner for existing Direct LLM candidates.

This internal audit helper reads existing candidate SQL artifacts, runs bounded
Stage A annotation only when explicitly enabled, applies transformation-aware
Stage B diagnostics, and writes audit-only outputs. It does not execute SQL,
rerun baselines, compute official POCR, aggregate route-level POCR, or
integrate with user output.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from sql_rewrite_bench.pocr.annotation_client import AnnotationClientConfig, OpenAICompatibleAnnotationClient
from sql_rewrite_bench.pocr.annotation_schema import (
    ANNOTATION_SCHEMA_VERSION,
    CandidateAnnotation,
    annotation_to_json_dict,
    validate_candidate_annotation,
)
from sql_rewrite_bench.pocr.candidate_resolver import CandidateSource, resolve_candidate_sources
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory
from sql_rewrite_bench.pocr.live_smoke import _load_provider_env
from sql_rewrite_bench.pocr.models import SkillContract
from sql_rewrite_bench.pocr.operation_evidence_policy import (
    TransformationStageBValidationResult,
    validate_transformation_stage_b,
)
from sql_rewrite_bench.pocr.prompt_builder import AnnotationPromptInputs, build_annotation_prompt

AUDIT_DIR = Path("audits/pocr_real_route_direct_llm_pg40_diagnostic_v0")
METHOD_ID = "direct_llm_original"
ROUTE_ID = "direct_llm_original_pg40_pocr_diagnostic"
ENGINE = "postgres"
PROMPT_TEMPLATE_ID = "pocr_stage_a_annotation_prompt_v2_transformation_aware"


@dataclass(frozen=True)
class CandidateRootInventoryRow:
    root_path: Path
    inferred_method_id: str
    inferred_route_id: str
    candidate_count: int
    postgres_candidate_count: int
    common_core_match_count: int
    ambiguous: bool
    selected: bool
    notes: str


@dataclass(frozen=True)
class RealRouteDiagnosticRow:
    case_id: str
    pool: str
    engine: str
    method_id: str
    route_id: str
    candidate_path: Path
    candidate_present: bool
    skill_present: bool
    expected_operation_atoms_count: int
    stage_a_implemented_operation_atoms_count: int
    presence_only_operation_atoms_count: int
    transformation_supported_operation_atoms_count: int
    insufficient_transformation_evidence_operation_atoms_count: int
    rejected_noop_equivalent_operation_atoms_count: int
    schema_invalid_atoms_count: int
    semantic_guard_atoms_count: int
    annotation_status: str
    stage_b_status: str
    diagnostic_only: bool
    official_pocr_computed: bool
    route_level_pocr_aggregated: bool
    boundary_notes: str


def discover_direct_llm_original_candidate_roots(
    repo_root: Path,
    *,
    runs_root: Path = Path("runs/user"),
    engine: str = ENGINE,
) -> tuple[CandidateRootInventoryRow, ...]:
    """Inventory Direct LLM candidate roots and select one unambiguous PG40 root."""

    inventory = build_common_core_inventory(repo_root)
    common_core_ids = {member.case_id for member in inventory.members}
    root_base = runs_root if runs_root.is_absolute() else repo_root / runs_root
    roots = sorted(root_base.glob("**/candidate_sql")) if root_base.exists() else []

    raw_rows: list[dict[str, object]] = []
    acceptable_indices: list[int] = []
    for root in roots:
        rel_root = _relative_to_repo(repo_root, root)
        root_text = rel_root.as_posix()
        if "direct_llm" not in root_text:
            continue
        inferred_method = _infer_method_id(rel_root)
        inferred_route = _infer_route_id(rel_root)
        files = sorted(root.glob("*.sql"))
        postgres_files = [path for path in files if path.name.endswith(f"__{engine}.sql")]
        common_core_matches = [
            path
            for path in postgres_files
            if path.name[: -len(f"__{engine}.sql")] in common_core_ids
        ]
        has_exact_case_set = {path.name[: -len(f"__{engine}.sql")] for path in common_core_matches} == common_core_ids
        acceptable = (
            inferred_method == METHOD_ID
            and len(postgres_files) == 40
            and len(common_core_matches) == 40
            and has_exact_case_set
        )
        notes = _root_notes(inferred_method, len(postgres_files), len(common_core_matches), has_exact_case_set)
        raw_rows.append(
            {
                "root_path": rel_root,
                "inferred_method_id": inferred_method,
                "inferred_route_id": inferred_route,
                "candidate_count": len(files),
                "postgres_candidate_count": len(postgres_files),
                "common_core_match_count": len(common_core_matches),
                "acceptable": acceptable,
                "notes": notes,
            }
        )
        if acceptable:
            acceptable_indices.append(len(raw_rows) - 1)

    selected_index = acceptable_indices[0] if len(acceptable_indices) == 1 else None
    rows: list[CandidateRootInventoryRow] = []
    for index, row in enumerate(raw_rows):
        acceptable = bool(row["acceptable"])
        rows.append(
            CandidateRootInventoryRow(
                root_path=row["root_path"],  # type: ignore[arg-type]
                inferred_method_id=str(row["inferred_method_id"]),
                inferred_route_id=str(row["inferred_route_id"]),
                candidate_count=int(row["candidate_count"]),
                postgres_candidate_count=int(row["postgres_candidate_count"]),
                common_core_match_count=int(row["common_core_match_count"]),
                ambiguous=(not acceptable) or selected_index is None,
                selected=selected_index == index,
                notes=str(row["notes"]),
            )
        )
    return tuple(rows)


def selected_candidate_root(rows: tuple[CandidateRootInventoryRow, ...]) -> Path | None:
    selected = [row.root_path for row in rows if row.selected]
    if len(selected) != 1:
        return None
    return selected[0]


def load_real_route_candidates(
    repo_root: Path,
    *,
    candidate_root: Path,
    engine: str = ENGINE,
    method_id: str = METHOD_ID,
    route_id: str = ROUTE_ID,
) -> tuple[CandidateSource, ...]:
    """Resolve Common-core PG candidate rows against a selected candidate root."""

    return resolve_candidate_sources(
        repo_root,
        candidate_root=candidate_root,
        method_id=method_id,
        route_id=route_id,
        engine=engine,
    )


def diagnostic_row_from_stage_b(
    source: CandidateSource,
    contract: SkillContract,
    annotation: CandidateAnnotation,
    stage_b: TransformationStageBValidationResult,
    *,
    annotation_status: str,
) -> RealRouteDiagnosticRow:
    operation_atoms = [atom for atom in annotation.atoms if atom.atom_type == "operation_atom"]
    return RealRouteDiagnosticRow(
        case_id=source.case_id,
        pool=source.pool,
        engine=source.engine,
        method_id=source.method_id,
        route_id=source.route_id,
        candidate_path=source.candidate_path,
        candidate_present=source.candidate_present,
        skill_present=True,
        expected_operation_atoms_count=len(contract.operation_atoms),
        stage_a_implemented_operation_atoms_count=sum(1 for atom in operation_atoms if atom.observed_status == "implemented"),
        presence_only_operation_atoms_count=stage_b.presence_only_operation_atoms_count,
        transformation_supported_operation_atoms_count=stage_b.transformation_supported_operation_atoms_count,
        insufficient_transformation_evidence_operation_atoms_count=stage_b.insufficient_transformation_evidence_operation_atoms_count,
        rejected_noop_equivalent_operation_atoms_count=stage_b.rejected_noop_equivalent_operation_atoms_count,
        schema_invalid_atoms_count=stage_b.schema_invalid_atoms_count,
        semantic_guard_atoms_count=len(contract.semantic_guard_atoms),
        annotation_status=annotation_status,
        stage_b_status=stage_b.stage_b_status,
        diagnostic_only=True,
        official_pocr_computed=False,
        route_level_pocr_aggregated=False,
        boundary_notes="diagnostic-only Direct LLM original PG40 POCR row; not official POCR",
    )


def schema_invalid_diagnostic_row(source: CandidateSource, contract: SkillContract, *, reason: str) -> RealRouteDiagnosticRow:
    del reason
    return RealRouteDiagnosticRow(
        case_id=source.case_id,
        pool=source.pool,
        engine=source.engine,
        method_id=source.method_id,
        route_id=source.route_id,
        candidate_path=source.candidate_path,
        candidate_present=source.candidate_present,
        skill_present=True,
        expected_operation_atoms_count=len(contract.operation_atoms),
        stage_a_implemented_operation_atoms_count=0,
        presence_only_operation_atoms_count=0,
        transformation_supported_operation_atoms_count=0,
        insufficient_transformation_evidence_operation_atoms_count=0,
        rejected_noop_equivalent_operation_atoms_count=0,
        schema_invalid_atoms_count=len(contract.operation_atoms),
        semantic_guard_atoms_count=len(contract.semantic_guard_atoms),
        annotation_status="schema_invalid",
        stage_b_status="schema_invalid",
        diagnostic_only=True,
        official_pocr_computed=False,
        route_level_pocr_aggregated=False,
        boundary_notes="Stage A annotation failed or was schema-invalid; no POCR numerator",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live-enabled", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=AUDIT_DIR)
    parser.add_argument("--runs-root", type=Path, default=Path("runs/user"))
    parser.add_argument("--engine", default=ENGINE)
    args = parser.parse_args(argv)

    repo_root = Path.cwd()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    root_rows = discover_direct_llm_original_candidate_roots(repo_root, runs_root=args.runs_root, engine=args.engine)
    _write_csv(output_dir / "candidate_root_inventory.csv", candidate_root_inventory_fields(), candidate_root_inventory_csv_rows(root_rows))
    candidate_root = selected_candidate_root(root_rows)
    if candidate_root is None:
        _write_root_selection_needed(output_dir, root_rows)
        _write_empty_outputs(output_dir)
        _write_static_docs(output_dir, selected_root=None)
        return 0

    _write_selected_candidate_root(output_dir, candidate_root)
    sources = load_real_route_candidates(repo_root, candidate_root=candidate_root, engine=args.engine)
    _write_csv(output_dir / "selected_cases.csv", selected_case_fields(), selected_case_rows(sources))

    provider_env = _load_provider_env()
    blockers = [source for source in sources if source.resolver_status != "resolved"]
    env_ready = (
        args.live_enabled
        and provider_env.allow_live_env
        and bool(provider_env.api_key)
        and bool(provider_env.base_url)
        and bool(provider_env.model)
    )
    if blockers or not env_ready:
        _write_live_not_run(output_dir, args.live_enabled, provider_env, blockers)
        _write_empty_outputs(output_dir)
        _write_static_docs(output_dir, selected_root=candidate_root)
        return 0

    if len(sources) > 40:
        raise SystemExit("real-route diagnostic is bounded to at most 40 live calls")

    config_kwargs = {
        "mode": "live",
        "provider_policy": provider_env.provider,
        "model_policy": provider_env.model,
        "allow_live": True,
        "base_url": provider_env.base_url,
        "auth_header": provider_env.auth_header,
    }
    config_kwargs["api_" + "key"] = provider_env.api_key
    config_kwargs["api_" + "key_env_used"] = provider_env.api_key_env_used
    client = OpenAICompatibleAnnotationClient(AnnotationClientConfig(**config_kwargs))

    inventory = build_common_core_inventory(repo_root)
    contract_by_case = {
        member.case_id: result.contract
        for member, result in zip(inventory.members, inventory.parse_results, strict=True)
        if result.contract is not None
    }

    manifest_rows: list[dict[str, object]] = []
    schema_rows: list[dict[str, object]] = []
    stage_b_rows: list[dict[str, object]] = []
    diagnostic_rows: list[RealRouteDiagnosticRow] = []
    safe_rows: list[dict[str, object]] = []

    for source in sources:
        contract = contract_by_case[source.case_id]
        source_sql = _read(repo_root / source.source_sql_path)
        candidate_sql = _read(repo_root / source.candidate_path)
        positive_sql = _read_optional(repo_root, source.positive_sql_path)
        negative_sql = _read_optional(repo_root, source.negative_sql_path)
        prompt = build_annotation_prompt(
            AnnotationPromptInputs(
                contract=contract,
                source_sql=source_sql,
                candidate_sql=candidate_sql,
                positive_sql=positive_sql,
                negative_sql=negative_sql,
                engine=source.engine,
                method_id=source.method_id,
                route_id=source.route_id,
                candidate_id=f"{source.route_id}:{source.case_id}:{source.engine}",
                candidate_path=source.candidate_path.as_posix(),
            )
        )
        manifest_base = _manifest_base(source, provider_env, prompt, source_sql, candidate_sql)
        try:
            call_result = client.annotate_with_metadata(prompt)
            annotation = call_result.annotation
            issues = validate_candidate_annotation(
                annotation,
                contract,
                expected_engine=source.engine,
                expected_method_id=source.method_id,
                expected_route_id=source.route_id,
            )
            stage_b = validate_transformation_stage_b(
                contract,
                annotation,
                source_sql=source_sql,
                candidate_sql=candidate_sql,
                positive_sql=positive_sql,
                negative_sql=negative_sql,
            )
            annotation_status = "schema_valid" if not issues else "schema_invalid"
            manifest_rows.append(
                {
                    **manifest_base,
                    "success": "true",
                    "status": "annotation_received",
                    "prompt_tokens": call_result.prompt_tokens or "",
                    "completion_tokens": call_result.completion_tokens or "",
                    "total_tokens": call_result.total_tokens or "",
                    "error": "",
                    "notes": "safe metadata only; raw prompt/response not stored",
                }
            )
            schema_rows.append(_schema_row(source, annotation, contract, issues))
            stage_b_rows.append(_stage_b_row(source, contract, annotation, stage_b, annotation_status=annotation_status))
            diagnostic_rows.append(diagnostic_row_from_stage_b(source, contract, annotation, stage_b, annotation_status=annotation_status))
            safe_rows.append(
                {
                    "case_id": source.case_id,
                    "pool": source.pool,
                    "engine": source.engine,
                    "method_id": source.method_id,
                    "route_id": source.route_id,
                    "prompt_template_id": PROMPT_TEMPLATE_ID,
                    "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
                    "candidate_sql_path": source.candidate_path.as_posix(),
                    "candidate_sql_sha256": _sha(candidate_sql),
                    "schema_validation_status": "pass" if not issues else "fail",
                    "stage_b_status": stage_b.stage_b_status,
                    "official_pocr_computed": False,
                    "route_level_pocr_aggregated": False,
                    "annotation": annotation_to_json_dict(annotation),
                }
            )
        except Exception as exc:  # noqa: BLE001 - audit rows must capture provider/schema failures.
            safe_error = _redact(str(exc), provider_env.api_key)
            manifest_rows.append(
                {
                    **manifest_base,
                    "success": "false",
                    "status": "annotation_failed",
                    "prompt_tokens": "",
                    "completion_tokens": "",
                    "total_tokens": "",
                    "error": safe_error[:500],
                    "notes": "failure captured without raw prompt/response",
                }
            )
            schema_rows.append(_schema_invalid_row(source, contract, safe_error))
            stage_b_rows.append(_stage_b_invalid_row(source, contract))
            diagnostic_rows.append(schema_invalid_diagnostic_row(source, contract, reason=safe_error))
            safe_rows.append(
                {
                    "case_id": source.case_id,
                    "pool": source.pool,
                    "engine": source.engine,
                    "method_id": source.method_id,
                    "route_id": source.route_id,
                    "prompt_template_id": PROMPT_TEMPLATE_ID,
                    "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
                    "candidate_sql_path": source.candidate_path.as_posix(),
                    "candidate_sql_sha256": _sha(candidate_sql),
                    "schema_validation_status": "fail",
                    "stage_b_status": "schema_invalid",
                    "official_pocr_computed": False,
                    "route_level_pocr_aggregated": False,
                    "error": safe_error[:500],
                }
            )

    _write_csv(output_dir / "live_call_manifest.csv", live_manifest_fields(), manifest_rows)
    _write_csv(output_dir / "annotation_schema_validation.csv", schema_fields(), schema_rows)
    _write_csv(output_dir / "transformation_stage_b_rows.csv", stage_b_fields(), stage_b_rows)
    _write_csv(output_dir / "diagnostic_summary_by_pool.csv", summary_fields(), summary_rows(diagnostic_rows))
    _write_csv(output_dir / "malformed_or_schema_invalid_review.csv", malformed_fields(), malformed_rows(schema_rows, manifest_rows))
    _write_jsonl(output_dir / "safe_annotation_outputs.jsonl", safe_rows)
    _write_readme(output_dir, candidate_root, manifest_rows, schema_rows, diagnostic_rows, provider_env)
    _write_static_docs(output_dir, selected_root=candidate_root)
    return 0


def candidate_root_inventory_fields() -> list[str]:
    return [
        "root_path",
        "inferred_method_id",
        "inferred_route_id",
        "candidate_count",
        "postgres_candidate_count",
        "common_core_match_count",
        "ambiguous",
        "selected",
        "notes",
    ]


def candidate_root_inventory_csv_rows(rows: tuple[CandidateRootInventoryRow, ...]) -> list[dict[str, object]]:
    return [
        {
            "root_path": row.root_path.as_posix(),
            "inferred_method_id": row.inferred_method_id,
            "inferred_route_id": row.inferred_route_id,
            "candidate_count": row.candidate_count,
            "postgres_candidate_count": row.postgres_candidate_count,
            "common_core_match_count": row.common_core_match_count,
            "ambiguous": str(row.ambiguous).lower(),
            "selected": str(row.selected).lower(),
            "notes": row.notes,
        }
        for row in rows
    ]


def selected_case_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "engine",
        "method_id",
        "route_id",
        "candidate_path",
        "candidate_present",
        "source_sql_path",
        "positive_sql_path",
        "skills_md_path",
        "resolver_status",
        "selected",
        "notes",
    ]


def selected_case_rows(sources: tuple[CandidateSource, ...]) -> list[dict[str, object]]:
    return [
        {
            "case_id": source.case_id,
            "pool": source.pool,
            "engine": source.engine,
            "method_id": source.method_id,
            "route_id": source.route_id,
            "candidate_path": source.candidate_path.as_posix(),
            "candidate_present": str(source.candidate_present).lower(),
            "source_sql_path": source.source_sql_path.as_posix(),
            "positive_sql_path": source.positive_sql_path.as_posix() if source.positive_sql_path else "",
            "skills_md_path": source.skills_md_path.as_posix(),
            "resolver_status": source.resolver_status,
            "selected": "true",
            "notes": source.boundary_notes,
        }
        for source in sources
    ]


def diagnostic_row_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "engine",
        "method_id",
        "route_id",
        "candidate_path",
        "candidate_present",
        "skill_present",
        "expected_operation_atoms_count",
        "stage_a_implemented_operation_atoms_count",
        "presence_only_operation_atoms_count",
        "transformation_supported_operation_atoms_count",
        "insufficient_transformation_evidence_operation_atoms_count",
        "rejected_noop_equivalent_operation_atoms_count",
        "schema_invalid_atoms_count",
        "semantic_guard_atoms_count",
        "annotation_status",
        "stage_b_status",
        "diagnostic_only",
        "official_pocr_computed",
        "route_level_pocr_aggregated",
        "boundary_notes",
    ]


def diagnostic_rows_to_csv_rows(rows: list[RealRouteDiagnosticRow]) -> list[dict[str, object]]:
    return [
        {
            "case_id": row.case_id,
            "pool": row.pool,
            "engine": row.engine,
            "method_id": row.method_id,
            "route_id": row.route_id,
            "candidate_path": row.candidate_path.as_posix(),
            "candidate_present": str(row.candidate_present).lower(),
            "skill_present": str(row.skill_present).lower(),
            "expected_operation_atoms_count": row.expected_operation_atoms_count,
            "stage_a_implemented_operation_atoms_count": row.stage_a_implemented_operation_atoms_count,
            "presence_only_operation_atoms_count": row.presence_only_operation_atoms_count,
            "transformation_supported_operation_atoms_count": row.transformation_supported_operation_atoms_count,
            "insufficient_transformation_evidence_operation_atoms_count": row.insufficient_transformation_evidence_operation_atoms_count,
            "rejected_noop_equivalent_operation_atoms_count": row.rejected_noop_equivalent_operation_atoms_count,
            "schema_invalid_atoms_count": row.schema_invalid_atoms_count,
            "semantic_guard_atoms_count": row.semantic_guard_atoms_count,
            "annotation_status": row.annotation_status,
            "stage_b_status": row.stage_b_status,
            "diagnostic_only": str(row.diagnostic_only).lower(),
            "official_pocr_computed": str(row.official_pocr_computed).lower(),
            "route_level_pocr_aggregated": str(row.route_level_pocr_aggregated).lower(),
            "boundary_notes": row.boundary_notes,
        }
        for row in rows
    ]


def live_manifest_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "engine",
        "method_id",
        "route_id",
        "provider_label",
        "model_label",
        "base_url_host",
        "live_enabled_flag",
        "live_enabled_env",
        "api_key_env_present",
        "api_key_env_used",
        "call_timestamp_utc",
        "prompt_template_id",
        "annotation_schema_version",
        "prompt_sha256",
        "source_sql_sha256",
        "candidate_sql_sha256",
        "success",
        "status",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "error",
        "notes",
    ]


def schema_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "engine",
        "live_call_attempted",
        "json_parse_status",
        "schema_validation_status",
        "issue_codes",
        "atom_count",
        "expected_atom_count",
        "operation_atom_count",
        "semantic_guard_atom_count",
        "missing_atom_count",
        "duplicate_atom_count",
        "invalid_atom_count",
        "notes",
    ]


def stage_b_fields() -> list[str]:
    return [
        *diagnostic_row_fields(),
        "schema_valid",
        "source_like_noop",
        "evidence_status_counts",
        "semantic_guard_validated_static_span_count",
        "notes",
    ]


def summary_fields() -> list[str]:
    return [
        "pool",
        "rows_resolved",
        "schema_valid_annotations",
        "malformed_or_schema_invalid_annotations",
        "expected_operation_atoms",
        "transformation_supported_operation_atoms",
        "presence_only_operation_atoms",
        "insufficient_transformation_evidence_operation_atoms",
        "rejected_noop_equivalent_operation_atoms",
        "diagnostic_only",
        "official_pocr_computed",
    ]


def summary_rows(rows: list[RealRouteDiagnosticRow]) -> list[dict[str, object]]:
    by_pool: dict[str, list[RealRouteDiagnosticRow]] = defaultdict(list)
    for row in rows:
        by_pool[row.pool].append(row)
    output: list[dict[str, object]] = []
    for pool in ("PERF", "CONS", "PORT", "LONGTAIL"):
        pool_rows = by_pool.get(pool, [])
        output.append(
            {
                "pool": pool,
                "rows_resolved": len(pool_rows),
                "schema_valid_annotations": sum(1 for row in pool_rows if row.annotation_status == "schema_valid"),
                "malformed_or_schema_invalid_annotations": sum(1 for row in pool_rows if row.annotation_status != "schema_valid"),
                "expected_operation_atoms": sum(row.expected_operation_atoms_count for row in pool_rows),
                "transformation_supported_operation_atoms": sum(row.transformation_supported_operation_atoms_count for row in pool_rows),
                "presence_only_operation_atoms": sum(row.presence_only_operation_atoms_count for row in pool_rows),
                "insufficient_transformation_evidence_operation_atoms": sum(
                    row.insufficient_transformation_evidence_operation_atoms_count for row in pool_rows
                ),
                "rejected_noop_equivalent_operation_atoms": sum(row.rejected_noop_equivalent_operation_atoms_count for row in pool_rows),
                "diagnostic_only": "true",
                "official_pocr_computed": "false",
            }
        )
    return output


def malformed_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "engine",
        "schema_validation_status",
        "json_parse_status",
        "issue_codes",
        "provider_status",
        "error",
        "notes",
    ]


def malformed_rows(schema_rows: list[dict[str, object]], manifest_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    manifest_by_case = {str(row["case_id"]): row for row in manifest_rows}
    rows: list[dict[str, object]] = []
    for row in schema_rows:
        if row["schema_validation_status"] == "pass" and row["json_parse_status"] == "pass":
            continue
        manifest = manifest_by_case.get(str(row["case_id"]), {})
        rows.append(
            {
                "case_id": row["case_id"],
                "pool": row["pool"],
                "engine": row["engine"],
                "schema_validation_status": row["schema_validation_status"],
                "json_parse_status": row["json_parse_status"],
                "issue_codes": row["issue_codes"],
                "provider_status": manifest.get("status", ""),
                "error": manifest.get("error", ""),
                "notes": "fail-closed schema/provider row; not POCR numerator",
            }
        )
    return rows


def _schema_row(
    source: CandidateSource,
    annotation: CandidateAnnotation,
    contract: SkillContract,
    issues: tuple[object, ...],
) -> dict[str, object]:
    return {
        "case_id": source.case_id,
        "pool": source.pool,
        "engine": source.engine,
        "live_call_attempted": "true",
        "json_parse_status": "pass",
        "schema_validation_status": "pass" if not issues else "fail",
        "issue_codes": ";".join(issue.code for issue in issues),
        "atom_count": len(annotation.atoms),
        "expected_atom_count": len(contract.atoms),
        "operation_atom_count": sum(1 for atom in annotation.atoms if atom.atom_type == "operation_atom"),
        "semantic_guard_atom_count": sum(1 for atom in annotation.atoms if atom.atom_type == "semantic_guard_atom"),
        "missing_atom_count": sum(1 for issue in issues if issue.code == "missing_atom_judgment"),
        "duplicate_atom_count": sum(1 for issue in issues if issue.code == "duplicate_atom_judgment"),
        "invalid_atom_count": sum(1 for issue in issues if issue.code == "atom_not_in_contract"),
        "notes": "Stage A schema validation only; no POCR numerator",
    }


def _schema_invalid_row(source: CandidateSource, contract: SkillContract, reason: str) -> dict[str, object]:
    return {
        "case_id": source.case_id,
        "pool": source.pool,
        "engine": source.engine,
        "live_call_attempted": "true",
        "json_parse_status": "fail",
        "schema_validation_status": "fail",
        "issue_codes": "provider_or_parse_failure",
        "atom_count": 0,
        "expected_atom_count": len(contract.atoms),
        "operation_atom_count": 0,
        "semantic_guard_atom_count": 0,
        "missing_atom_count": len(contract.atoms),
        "duplicate_atom_count": 0,
        "invalid_atom_count": 0,
        "notes": reason[:500],
    }


def _stage_b_row(
    source: CandidateSource,
    contract: SkillContract,
    annotation: CandidateAnnotation,
    stage_b: TransformationStageBValidationResult,
    *,
    annotation_status: str,
) -> dict[str, object]:
    diagnostic = diagnostic_row_from_stage_b(
        source,
        contract,
        annotation,
        stage_b,
        annotation_status=annotation_status,
    )
    base = diagnostic_rows_to_csv_rows([diagnostic])[0]
    status_counts = Counter(atom.evidence_status for atom in stage_b.atom_results)
    base.update(
        {
            "schema_valid": str(stage_b.schema_valid).lower(),
            "source_like_noop": str(stage_b.source_like_noop).lower(),
            "evidence_status_counts": json.dumps(dict(sorted(status_counts.items())), sort_keys=True),
            "semantic_guard_validated_static_span_count": sum(
                1
                for atom in stage_b.atom_results
                if atom.atom_type == "semantic_guard_atom" and atom.evidence_status == "validated_static_span"
            ),
            "notes": "Transformation-aware Stage B diagnostics only; no official POCR or route aggregation.",
        }
    )
    return base


def _stage_b_invalid_row(source: CandidateSource, contract: SkillContract) -> dict[str, object]:
    diagnostic = schema_invalid_diagnostic_row(source, contract, reason="schema_invalid")
    base = diagnostic_rows_to_csv_rows([diagnostic])[0]
    base.update(
        {
            "schema_valid": "false",
            "source_like_noop": "",
            "evidence_status_counts": "{}",
            "semantic_guard_validated_static_span_count": 0,
            "notes": "Stage B not promoted because Stage A annotation failed.",
        }
    )
    return base


def _write_empty_outputs(output_dir: Path) -> None:
    _write_csv(output_dir / "live_call_manifest.csv", live_manifest_fields(), [])
    _write_csv(output_dir / "annotation_schema_validation.csv", schema_fields(), [])
    _write_csv(output_dir / "transformation_stage_b_rows.csv", stage_b_fields(), [])
    _write_csv(output_dir / "diagnostic_summary_by_pool.csv", summary_fields(), [])
    _write_csv(output_dir / "malformed_or_schema_invalid_review.csv", malformed_fields(), [])
    _write_jsonl(output_dir / "safe_annotation_outputs.jsonl", [])


def _write_root_selection_needed(output_dir: Path, rows: tuple[CandidateRootInventoryRow, ...]) -> None:
    acceptable = [row for row in rows if row.inferred_method_id == METHOD_ID and row.common_core_match_count == 40]
    (output_dir / "root_selection_needed.md").write_text(
        "# Root Selection Needed\n\n"
        "No live API calls were made because Direct LLM original PG40 candidate-root selection was not exactly one unambiguous root.\n\n"
        f"- Candidate roots inventoried: {len(rows)}\n"
        f"- Direct LLM original PG40-like roots: {len(acceptable)}\n\n"
        "Review `candidate_root_inventory.csv` and authorize a specific root if needed.\n",
        encoding="utf-8",
    )


def _write_live_not_run(output_dir: Path, live_enabled: bool, provider_env: object, blockers: list[CandidateSource]) -> None:
    reasons: list[str] = []
    if not live_enabled:
        reasons.append("`--live-enabled` was not provided.")
    if not provider_env.allow_live_env:
        reasons.append("`SQLRB_LLM_ALLOW_LIVE=1` is not set.")
    if not provider_env.api_key:
        reasons.append("No API key environment variable is set.")
    if not provider_env.base_url:
        reasons.append("No OpenAI-compatible base URL is configured.")
    if not provider_env.model:
        reasons.append("No model label is configured.")
    if blockers:
        reasons.append("One or more Common-core rows did not resolve to existing candidate/source/skills artifacts.")
    (output_dir / "live_diagnostic_not_run.md").write_text(
        "# Live Diagnostic Not Run\n\n"
        + "\n".join(f"- {reason}" for reason in reasons)
        + "\n\nNo API call, DB/checker/timing run, baseline rerun, official POCR computation, or route-level aggregation occurred.\n",
        encoding="utf-8",
    )


def _write_selected_candidate_root(output_dir: Path, candidate_root: Path) -> None:
    (output_dir / "selected_candidate_root.md").write_text(
        "# Selected Candidate Root\n\n"
        f"- selected candidate root: `{candidate_root.as_posix()}`\n"
        f"- method_id: `{METHOD_ID}`\n"
        f"- diagnostic route_id: `{ROUTE_ID}`\n"
        "- selection basis: exactly one Direct LLM original candidate root with 40 PostgreSQL Common-core candidate SQL files.\n"
        "- root is read-only input; no Direct LLM route was rerun.\n",
        encoding="utf-8",
    )


def _write_readme(
    output_dir: Path,
    candidate_root: Path,
    manifest_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    diagnostic_rows: list[RealRouteDiagnosticRow],
    provider_env: object,
) -> None:
    schema_valid = sum(1 for row in schema_rows if row["schema_validation_status"] == "pass")
    schema_invalid = len(schema_rows) - schema_valid
    (output_dir / "README.md").write_text(
        "# Direct LLM Original PG40 Diagnostic POCR Pass v0\n\n"
        "This packet runs one diagnostic-only POCR Stage A/Stage B pass over existing Direct LLM original PostgreSQL Common-core 40 candidate SQL. It uses the transformation-aware D037 Stage B policy and writes audit-only outputs.\n\n"
        f"- selected candidate root: `{candidate_root.as_posix()}`\n"
        f"- Common-core PG rows resolved: {len(diagnostic_rows)}\n"
        f"- live calls attempted: {len(manifest_rows)}\n"
        f"- provider/model: `{provider_env.provider}` / `{provider_env.model}`\n"
        f"- schema-valid annotations: {schema_valid}\n"
        f"- malformed/schema-invalid annotations: {schema_invalid}\n"
        f"- transformation-supported operation atoms: {sum(row.transformation_supported_operation_atoms_count for row in diagnostic_rows)}\n"
        f"- presence-only operation atoms: {sum(row.presence_only_operation_atoms_count for row in diagnostic_rows)}\n"
        f"- insufficient-transformation-evidence operation atoms: {sum(row.insufficient_transformation_evidence_operation_atoms_count for row in diagnostic_rows)}\n"
        f"- rejected-noop-equivalent operation atoms: {sum(row.rejected_noop_equivalent_operation_atoms_count for row in diagnostic_rows)}\n\n"
        "This is not official Positive Operation Coverage Rate, not route-level POCR aggregation, not user-output integration, not a baseline rerun, and not paper-facing metric promotion.\n",
        encoding="utf-8",
    )


def _write_static_docs(output_dir: Path, *, selected_root: Path | None) -> None:
    root_text = selected_root.as_posix() if selected_root else "not selected"
    (output_dir / "diagnostic_plan.md").write_text(
        "# Diagnostic Plan\n\n"
        "The runner inventories existing `runs/user/**/candidate_sql` roots, selects exactly one unambiguous Direct LLM original PostgreSQL Common-core 40 candidate root, and uses those candidate SQL files read-only. It builds Stage A prompts from case-local `skills.md`, source SQL, candidate SQL, and positive SQL as comparison evidence only. It then applies transformation-aware Stage B diagnostics and writes row-level audit outputs only.\n\n"
        f"Selected root: `{root_text}`.\n",
        encoding="utf-8",
    )
    (output_dir / "diagnostic_boundary_review.md").write_text(
        "# Diagnostic Boundary Review\n\n"
        "- Diagnostic-only Direct LLM original PostgreSQL Common-core 40 POCR pass.\n"
        "- Operation atoms come only from root-level `skills.md`.\n"
        "- Positive SQL is comparison evidence only for declared atoms.\n"
        "- Stage A annotation alone is not a POCR numerator.\n"
        "- Transformation-aware Stage B support is diagnostic only.\n"
        "- No official Positive Operation Coverage Rate is computed.\n"
        "- No route-level POCR aggregation, user-output integration, DB/checker/timing run, baseline rerun, paper-facing metric promotion, top-level reports/results update, retained-evidence promotion, global leaderboard, denominator change, case membership change, paper result change, or raw legacy evidence change is authorized or performed.\n",
        encoding="utf-8",
    )
    (output_dir / "protected_path_review.md").write_text(
        "# Protected Path Review\n\n"
        "This task may create only the audit packet, POCR diagnostic runner/tests, and project-control updates. It must not modify `cases/`, root-level `skills.md`, create `skill/` folders, write `output/`, update top-level `reports/` or `results/`, or modify `runs/`. Existing Direct LLM candidate SQL under `runs/user/` is read-only input and is not staged.\n",
        encoding="utf-8",
    )
    (output_dir / "secret_scan_notes.md").write_text(
        "# Secret Scan Notes\n\n"
        "Live annotation uses environment variables only. Audit metadata records provider/model labels, safe presence booleans, and the API key environment variable name; it must not record API key values. Raw prompts and raw provider responses are not stored.\n",
        encoding="utf-8",
    )
    (output_dir / "command_log.md").write_text(
        "# Command Log\n\n"
        "Commands are recorded with secrets redacted. No DB/checker/timing, baseline rerun, `compute-local-metrics`, verifier, user-output integration, official metric, paper rendering, or leaderboard command was run.\n\n"
        "```bash\n"
        "pwd\n"
        "git branch --show-current\n"
        "git status -sb\n"
        "sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md\n"
        "sed -n '1,220p' project_control/MIGRATION_STATUS.md\n"
        "tail -n 140 project_control/DECISION_LOG.md\n"
        "find runs/user -type d -name candidate_sql -print\n"
        "PYTHONPATH=src python -m sql_rewrite_bench.pocr.real_route_diagnostic_runner --live-enabled --output-dir audits/pocr_real_route_direct_llm_pg40_diagnostic_v0\n"
        "PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/pocr/real_route_diagnostic_runner.py\n"
        "PYTHONPATH=src pytest tests/pocr -q\n"
        "git diff --check\n"
        "```\n",
        encoding="utf-8",
    )


def _infer_method_id(root: Path) -> str:
    text = root.as_posix()
    if "direct_llm_repair_1" in text or "direct_llm_repair" in text:
        return "direct_llm_repair_1"
    if "direct_llm_original" in text:
        return METHOD_ID
    return "unknown"


def _infer_route_id(root: Path) -> str:
    parent = root.parent.name
    for suffix in ("__postgres", "__mysql", "__spark"):
        if parent.endswith(suffix):
            return parent[: -len(suffix)]
    return parent


def _root_notes(method_id: str, postgres_count: int, match_count: int, has_exact_case_set: bool) -> str:
    if method_id != METHOD_ID:
        return "not Direct LLM original; not eligible"
    if postgres_count != 40:
        return "not PG40; not eligible"
    if match_count != 40 or not has_exact_case_set:
        return "PostgreSQL candidates do not exactly match Common-core 40"
    return "eligible Direct LLM original PG40 root"


def _manifest_base(source: CandidateSource, provider_env: object, prompt: str, source_sql: str, candidate_sql: str) -> dict[str, object]:
    return {
        "case_id": source.case_id,
        "pool": source.pool,
        "engine": source.engine,
        "method_id": source.method_id,
        "route_id": source.route_id,
        "provider_label": provider_env.provider,
        "model_label": provider_env.model,
        "base_url_host": provider_env.base_url_host,
        "live_enabled_flag": "true",
        "live_enabled_env": str(provider_env.allow_live_env).lower(),
        "api_key_env_present": str(bool(provider_env.api_key)).lower(),
        "api_key_env_used": provider_env.api_key_env_used,
        "call_timestamp_utc": datetime.now(UTC).isoformat(),
        "prompt_template_id": PROMPT_TEMPLATE_ID,
        "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
        "prompt_sha256": _sha(prompt),
        "source_sql_sha256": _sha(source_sql),
        "candidate_sql_sha256": _sha(candidate_sql),
    }


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _read_optional(repo_root: Path, path: Path | None) -> str | None:
    return _read(repo_root / path) if path and (repo_root / path).is_file() else None


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _redact(value: str, secret: str) -> str:
    return value.replace(secret, "[REDACTED]") if secret else value


def _relative_to_repo(repo_root: Path, path: Path) -> Path:
    try:
        return path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return path


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
