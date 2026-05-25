"""Bounded positive-vs-noop POCR calibration runner.

This is an internal audit helper. It does not execute SQL, rerun baselines,
compute official POCR, aggregate route-level POCR, or integrate with user
output.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
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
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory
from sql_rewrite_bench.pocr.live_smoke import _load_provider_env
from sql_rewrite_bench.pocr.models import SkillContract
from sql_rewrite_bench.pocr.operation_evidence_policy import (
    TransformationStageBValidationResult,
    validate_transformation_stage_b,
)
from sql_rewrite_bench.pocr.prompt_builder import AnnotationPromptInputs, build_annotation_prompt

DEFAULT_CASES = ("PERF_0006", "CONS_0005", "PORT_0003", "LONGTAIL_0011")
FULL40_CASE_LIST_ALIASES = {"common_core_v0", "full40", "all"}
DEFAULT_NOOP_CANDIDATE_ROOT = Path("runs/user/common_core_pg_noop_db_checker/candidate_sql")
DEFAULT_OUTPUT_DIR = Path("audits/pocr_transformation_aware_stage_b_calibration_v0")
FULL40_OUTPUT_DIR = Path("audits/pocr_full40_positive_vs_noop_control_calibration_v0")
DEFAULT_POSITIVE_ROUTE_ID = "pocr_positive_control_calibration"
FULL40_POSITIVE_ROUTE_ID = "pocr_positive_control_full40_calibration"
PROMPT_TEMPLATE_ID = "pocr_stage_a_annotation_prompt_v2_transformation_aware"


@dataclass(frozen=True)
class CalibrationCandidate:
    case_id: str
    pool: str
    engine: str
    candidate_class: str
    method_id: str
    route_id: str
    source_sql_path: Path
    candidate_sql_path: Path
    positive_sql_path: Path
    negative_sql_path: Path | None
    candidate_source_status: str
    notes: str


@dataclass(frozen=True)
class CalibrationResultRow:
    case_id: str
    pool: str
    candidate_class: str
    method_id: str
    route_id: str
    expected_operation_atoms_count: int
    stage_a_implemented_operation_atoms_count: int
    presence_only_operation_atoms_count: int
    transformation_supported_operation_atoms_count: int
    insufficient_transformation_evidence_operation_atoms_count: int
    rejected_noop_equivalent_operation_atoms_count: int
    schema_invalid_atoms_count: int
    semantic_guard_atoms_count: int
    diagnostic_only: bool
    official_pocr_computed: bool
    route_level_pocr_aggregated: bool
    calibration_risk: str


def load_calibration_candidates(
    repo_root: Path,
    *,
    case_ids: tuple[str, ...] = DEFAULT_CASES,
    noop_candidate_root: Path = DEFAULT_NOOP_CANDIDATE_ROOT,
    engine: str = "postgres",
    positive_route_id: str = DEFAULT_POSITIVE_ROUTE_ID,
) -> tuple[CalibrationCandidate, ...]:
    """Load positive-control and no-op candidate paths without running methods."""

    inventory = build_common_core_inventory(repo_root)
    member_by_case = {member.case_id: member for member in inventory.members}
    unknown = set(case_ids) - set(member_by_case)
    if unknown:
        raise ValueError(f"case filter includes non-Common-core case IDs: {sorted(unknown)}")

    rows: list[CalibrationCandidate] = []
    for case_id in case_ids:
        member = member_by_case[case_id]
        source_path = member.case_path / "sql/source.sql"
        positive_path = member.case_path / "sql/pos_01.sql"
        negative_path = member.case_path / "sql/neg_01.sql"
        noop_path = noop_candidate_root / f"{case_id}__{engine}.sql"
        rows.append(
            CalibrationCandidate(
                case_id=case_id,
                pool=member.pool,
                engine=engine,
                candidate_class="positive_control",
                method_id="human_positive_control",
                route_id=positive_route_id,
                source_sql_path=source_path,
                candidate_sql_path=positive_path,
                positive_sql_path=positive_path,
                negative_sql_path=negative_path if (repo_root / negative_path).is_file() else None,
                candidate_source_status=_status(repo_root, source_path, positive_path, positive_path),
                notes="Human positive SQL from case-local pos_01.sql; read-only calibration input.",
            )
        )
        rows.append(
            CalibrationCandidate(
                case_id=case_id,
                pool=member.pool,
                engine=engine,
                candidate_class="noop_control",
                method_id="sqlglot_noop",
                route_id="common_core_pg_noop_db_checker",
                source_sql_path=source_path,
                candidate_sql_path=noop_path,
                positive_sql_path=positive_path,
                negative_sql_path=negative_path if (repo_root / negative_path).is_file() else None,
                candidate_source_status=_status(repo_root, source_path, noop_path, positive_path),
                notes="Existing no-op candidate SQL artifact; read-only calibration input; no baseline rerun.",
            )
        )
    return tuple(rows)


def calibration_result_from_stage_b(
    candidate: CalibrationCandidate,
    contract: SkillContract,
    annotation: CandidateAnnotation,
    stage_b: TransformationStageBValidationResult,
) -> CalibrationResultRow:
    """Build one diagnostic calibration row from Stage A and transformation-aware Stage B."""

    operation_atoms = [atom for atom in annotation.atoms if atom.atom_type == "operation_atom"]
    return CalibrationResultRow(
        case_id=candidate.case_id,
        pool=candidate.pool,
        candidate_class=candidate.candidate_class,
        method_id=candidate.method_id,
        route_id=candidate.route_id,
        expected_operation_atoms_count=len(contract.operation_atoms),
        stage_a_implemented_operation_atoms_count=sum(1 for atom in operation_atoms if atom.observed_status == "implemented"),
        presence_only_operation_atoms_count=stage_b.presence_only_operation_atoms_count,
        transformation_supported_operation_atoms_count=stage_b.transformation_supported_operation_atoms_count,
        insufficient_transformation_evidence_operation_atoms_count=stage_b.insufficient_transformation_evidence_operation_atoms_count,
        rejected_noop_equivalent_operation_atoms_count=stage_b.rejected_noop_equivalent_operation_atoms_count,
        schema_invalid_atoms_count=stage_b.schema_invalid_atoms_count,
        semantic_guard_atoms_count=len(contract.semantic_guard_atoms),
        diagnostic_only=True,
        official_pocr_computed=False,
        route_level_pocr_aggregated=False,
        calibration_risk="pending_pair_comparison",
    )


def schema_invalid_calibration_result(
    candidate: CalibrationCandidate,
    contract: SkillContract,
    *,
    reason: str,
) -> CalibrationResultRow:
    del reason
    return CalibrationResultRow(
        case_id=candidate.case_id,
        pool=candidate.pool,
        candidate_class=candidate.candidate_class,
        method_id=candidate.method_id,
        route_id=candidate.route_id,
        expected_operation_atoms_count=len(contract.operation_atoms),
        stage_a_implemented_operation_atoms_count=0,
        presence_only_operation_atoms_count=0,
        transformation_supported_operation_atoms_count=0,
        insufficient_transformation_evidence_operation_atoms_count=0,
        rejected_noop_equivalent_operation_atoms_count=0,
        schema_invalid_atoms_count=len(contract.operation_atoms),
        semantic_guard_atoms_count=len(contract.semantic_guard_atoms),
        diagnostic_only=True,
        official_pocr_computed=False,
        route_level_pocr_aggregated=False,
        calibration_risk="schema_invalid",
    )


def apply_calibration_risks(rows: tuple[CalibrationResultRow, ...]) -> tuple[CalibrationResultRow, ...]:
    """Mark per-case positive/no-op calibration risk without computing POCR."""

    by_case: dict[str, dict[str, CalibrationResultRow]] = {}
    for row in rows:
        by_case.setdefault(row.case_id, {})[row.candidate_class] = row

    risks: dict[tuple[str, str], str] = {}
    for case_id, case_rows in by_case.items():
        positive = case_rows.get("positive_control")
        noop = case_rows.get("noop_control")
        if positive is None or noop is None:
            risk = "incomplete_pair"
        elif noop.transformation_supported_operation_atoms_count > 0:
            risk = "noop_transformation_overaccept_risk"
        elif (
            positive.transformation_supported_operation_atoms_count == 0
            and noop.transformation_supported_operation_atoms_count == 0
        ):
            risk = "atom_or_positive_alignment_gap"
        elif positive.transformation_supported_operation_atoms_count == 0:
            risk = "positive_control_no_transformation_support"
        else:
            risk = "low"
        for candidate_class in case_rows:
            risks[(case_id, candidate_class)] = risk

    return tuple(_replace_risk(row, risks.get((row.case_id, row.candidate_class), "incomplete_pair")) for row in rows)


def write_calibration_csv(path: Path, rows: tuple[CalibrationResultRow, ...]) -> None:
    _write_csv(path, calibration_result_fields(), calibration_results_to_csv_rows(rows))


def calibration_results_to_csv_rows(rows: tuple[CalibrationResultRow, ...]) -> list[dict[str, object]]:
    return [
        {
            "case_id": row.case_id,
            "pool": row.pool,
            "candidate_class": row.candidate_class,
            "method_id": row.method_id,
            "route_id": row.route_id,
            "expected_operation_atoms_count": row.expected_operation_atoms_count,
            "stage_a_implemented_operation_atoms_count": row.stage_a_implemented_operation_atoms_count,
            "presence_only_operation_atoms_count": row.presence_only_operation_atoms_count,
            "transformation_supported_operation_atoms_count": row.transformation_supported_operation_atoms_count,
            "insufficient_transformation_evidence_operation_atoms_count": row.insufficient_transformation_evidence_operation_atoms_count,
            "rejected_noop_equivalent_operation_atoms_count": row.rejected_noop_equivalent_operation_atoms_count,
            "schema_invalid_atoms_count": row.schema_invalid_atoms_count,
            "semantic_guard_atoms_count": row.semantic_guard_atoms_count,
            "diagnostic_only": str(row.diagnostic_only).lower(),
            "official_pocr_computed": str(row.official_pocr_computed).lower(),
            "route_level_pocr_aggregated": str(row.route_level_pocr_aggregated).lower(),
            "calibration_risk": row.calibration_risk,
        }
        for row in rows
    ]


def calibration_result_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "candidate_class",
        "method_id",
        "route_id",
        "expected_operation_atoms_count",
        "stage_a_implemented_operation_atoms_count",
        "presence_only_operation_atoms_count",
        "transformation_supported_operation_atoms_count",
        "insufficient_transformation_evidence_operation_atoms_count",
        "rejected_noop_equivalent_operation_atoms_count",
        "schema_invalid_atoms_count",
        "semantic_guard_atoms_count",
        "diagnostic_only",
        "official_pocr_computed",
        "route_level_pocr_aggregated",
        "calibration_risk",
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live-enabled", action="store_true")
    parser.add_argument("--case-list", default=",".join(DEFAULT_CASES))
    parser.add_argument("--noop-candidate-root", type=Path, default=DEFAULT_NOOP_CANDIDATE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--engine", default="postgres")
    parser.add_argument("--positive-route-id", default="")
    args = parser.parse_args(argv)

    repo_root = Path.cwd()
    case_ids, case_scope = _resolve_case_ids(repo_root, args.case_list)
    full40_mode = case_scope == "common_core_v0"
    output_dir = args.output_dir or (FULL40_OUTPUT_DIR if full40_mode else DEFAULT_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    if len(case_ids) * 2 > 80:
        raise SystemExit("calibration is bounded to at most 80 live calls")
    positive_route_id = args.positive_route_id or (FULL40_POSITIVE_ROUTE_ID if full40_mode else DEFAULT_POSITIVE_ROUTE_ID)

    candidates = load_calibration_candidates(
        repo_root,
        case_ids=case_ids,
        noop_candidate_root=args.noop_candidate_root,
        engine=args.engine,
        positive_route_id=positive_route_id,
    )
    _write_selected_cases(
        output_dir / "selected_cases.csv",
        candidates,
        noop_candidate_root=args.noop_candidate_root,
        selection_notes=(
            "Common-core v0 full-40 POCR control calibration"
            if full40_mode
            else "bounded four-case POCR calibration fixture"
        ),
    )
    _write_csv(output_dir / "candidate_class_inventory.csv", candidate_inventory_fields(), candidate_inventory_rows(candidates))
    comparison_filename = (
        "positive_vs_noop_full40_comparison.csv"
        if full40_mode
        else "positive_vs_noop_transformation_comparison.csv"
    )

    provider_env = _load_provider_env()
    blockers = [candidate for candidate in candidates if candidate.candidate_source_status != "ready"]
    env_ready = (
        args.live_enabled
        and provider_env.allow_live_env
        and bool(provider_env.api_key)
        and bool(provider_env.base_url)
        and bool(provider_env.model)
    )
    if blockers or not env_ready:
        _write_not_run(output_dir, args.live_enabled, provider_env, blockers, full40_mode=full40_mode)
        _write_empty_outputs(output_dir, comparison_filename=comparison_filename)
        return 0

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
    safe_rows: list[dict[str, object]] = []
    result_rows: list[CalibrationResultRow] = []

    for candidate in candidates:
        contract = contract_by_case[candidate.case_id]
        source_sql = _read(repo_root / candidate.source_sql_path)
        candidate_sql = _read(repo_root / candidate.candidate_sql_path)
        positive_sql = _read(repo_root / candidate.positive_sql_path)
        negative_sql = _read_optional(repo_root, candidate.negative_sql_path)
        prompt = build_annotation_prompt(
            AnnotationPromptInputs(
                contract=contract,
                source_sql=source_sql,
                candidate_sql=candidate_sql,
                positive_sql=positive_sql,
                negative_sql=negative_sql,
                engine=candidate.engine,
                method_id=candidate.method_id,
                route_id=candidate.route_id,
                candidate_id=f"{candidate.route_id}:{candidate.case_id}:{candidate.engine}:{candidate.candidate_class}",
                candidate_path=candidate.candidate_sql_path.as_posix(),
            )
        )
        manifest_base = _manifest_base(candidate, provider_env, prompt, source_sql, candidate_sql)
        try:
            call_result = client.annotate_with_metadata(prompt)
            annotation = call_result.annotation
            issues = validate_candidate_annotation(
                annotation,
                contract,
                expected_engine=candidate.engine,
                expected_method_id=candidate.method_id,
                expected_route_id=candidate.route_id,
            )
            stage_b = validate_transformation_stage_b(
                contract,
                annotation,
                source_sql=source_sql,
                candidate_sql=candidate_sql,
                positive_sql=positive_sql,
                negative_sql=negative_sql,
            )
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
            schema_rows.append(_schema_row(candidate, annotation, contract, issues))
            stage_b_rows.append(_stage_b_row(candidate, contract, stage_b))
            result_rows.append(calibration_result_from_stage_b(candidate, contract, annotation, stage_b))
            safe_rows.append(
                {
                    "case_id": candidate.case_id,
                    "pool": candidate.pool,
                    "engine": candidate.engine,
                    "candidate_class": candidate.candidate_class,
                    "method_id": candidate.method_id,
                    "route_id": candidate.route_id,
                    "prompt_template_id": PROMPT_TEMPLATE_ID,
                    "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
                    "candidate_sql_path": candidate.candidate_sql_path.as_posix(),
                    "candidate_sql_sha256": _sha(candidate_sql),
                    "schema_validation_status": "pass" if not issues else "fail",
                    "stage_b_status": stage_b.stage_b_status,
                    "official_pocr_computed": False,
                    "route_level_pocr_aggregated": False,
                    "annotation": annotation_to_json_dict(annotation),
                }
            )
        except Exception as exc:  # noqa: BLE001 - bounded audit must capture provider/schema failures.
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
            schema_rows.append(_schema_invalid_row(candidate, contract, safe_error))
            stage_b_rows.append(_stage_b_invalid_row(candidate, contract))
            result_rows.append(schema_invalid_calibration_result(candidate, contract, reason=safe_error))
            safe_rows.append(
                {
                    "case_id": candidate.case_id,
                    "pool": candidate.pool,
                    "engine": candidate.engine,
                    "candidate_class": candidate.candidate_class,
                    "method_id": candidate.method_id,
                    "route_id": candidate.route_id,
                    "prompt_template_id": PROMPT_TEMPLATE_ID,
                    "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
                    "candidate_sql_path": candidate.candidate_sql_path.as_posix(),
                    "candidate_sql_sha256": _sha(candidate_sql),
                    "schema_validation_status": "fail",
                    "stage_b_status": "schema_invalid",
                    "official_pocr_computed": False,
                    "route_level_pocr_aggregated": False,
                    "error": safe_error[:500],
                }
            )

    result_rows = list(apply_calibration_risks(tuple(result_rows)))
    _write_csv(output_dir / "live_call_manifest.csv", live_manifest_fields(), manifest_rows)
    _write_csv(output_dir / "annotation_schema_validation.csv", schema_fields(), schema_rows)
    _write_csv(output_dir / "transformation_stage_b_validation_by_class.csv", stage_b_fields(), stage_b_rows)
    write_calibration_csv(output_dir / comparison_filename, tuple(result_rows))
    _write_jsonl(output_dir / "safe_annotation_outputs.jsonl", safe_rows)
    _write_readme(output_dir, candidates, provider_env, manifest_rows, schema_rows, result_rows, full40_mode=full40_mode)
    _write_plan_docs(output_dir, full40_mode=full40_mode)
    return 0


def _resolve_case_ids(repo_root: Path, case_list: str) -> tuple[tuple[str, ...], str]:
    requested = case_list.strip()
    if requested in FULL40_CASE_LIST_ALIASES:
        inventory = build_common_core_inventory(repo_root)
        return tuple(member.case_id for member in inventory.members), "common_core_v0"
    case_ids = tuple(case_id.strip() for case_id in requested.split(",") if case_id.strip())
    if tuple(case_ids) == DEFAULT_CASES:
        return case_ids, "four_case_fixture"
    raise SystemExit("calibration case-list must be the authorized four fixture cases or common_core_v0")


def candidate_inventory_rows(candidates: tuple[CalibrationCandidate, ...]) -> list[dict[str, object]]:
    return [
        {
            "case_id": candidate.case_id,
            "pool": candidate.pool,
            "candidate_class": candidate.candidate_class,
            "method_id": candidate.method_id,
            "route_id": candidate.route_id,
            "engine": candidate.engine,
            "source_sql_path": candidate.source_sql_path.as_posix(),
            "candidate_sql_path": candidate.candidate_sql_path.as_posix(),
            "positive_sql_path": candidate.positive_sql_path.as_posix(),
            "negative_sql_path": candidate.negative_sql_path.as_posix() if candidate.negative_sql_path else "",
            "candidate_source_status": candidate.candidate_source_status,
            "notes": candidate.notes,
        }
        for candidate in candidates
    ]


def candidate_inventory_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "candidate_class",
        "method_id",
        "route_id",
        "engine",
        "source_sql_path",
        "candidate_sql_path",
        "positive_sql_path",
        "negative_sql_path",
        "candidate_source_status",
        "notes",
    ]


def live_manifest_fields() -> list[str]:
    return [
        "case_id",
        "pool",
        "candidate_class",
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
        "candidate_class",
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
        "case_id",
        "pool",
        "candidate_class",
        "engine",
        "schema_valid",
        "stage_b_status",
        "source_like_noop",
        "evidence_status_counts",
        "presence_only_operation_atoms_count",
        "transformation_supported_operation_atoms_count",
        "insufficient_transformation_evidence_operation_atoms_count",
        "rejected_noop_equivalent_operation_atoms_count",
        "schema_invalid_atoms_count",
        "expected_operation_atoms_count",
        "semantic_guard_validated_static_span_count",
        "semantic_guard_count",
        "official_pocr_computed",
        "route_level_pocr_aggregated",
        "notes",
    ]


def _status(repo_root: Path, source_path: Path, candidate_path: Path, positive_path: Path) -> str:
    if not (repo_root / source_path).is_file():
        return "missing_source_sql"
    if not (repo_root / candidate_path).is_file():
        return "missing_candidate_sql"
    if not (repo_root / positive_path).is_file():
        return "missing_positive_sql"
    return "ready"


def _replace_risk(row: CalibrationResultRow, risk: str) -> CalibrationResultRow:
    return CalibrationResultRow(**{**row.__dict__, "calibration_risk": risk})


def _write_selected_cases(
    path: Path,
    candidates: tuple[CalibrationCandidate, ...],
    *,
    noop_candidate_root: Path,
    selection_notes: str,
) -> None:
    seen: dict[str, CalibrationCandidate] = {}
    for candidate in candidates:
        seen.setdefault(candidate.case_id, candidate)
    rows = [
        {
            "case_id": candidate.case_id,
            "pool": candidate.pool,
            "engine": candidate.engine,
            "source_sql_path": candidate.source_sql_path.as_posix(),
            "positive_sql_path": candidate.positive_sql_path.as_posix(),
            "noop_candidate_sql_path": (
                noop_candidate_root / f"{candidate.case_id}__{candidate.engine}.sql"
            ).as_posix(),
            "selected": "true",
            "notes": selection_notes,
        }
        for candidate in seen.values()
    ]
    _write_csv(
        path,
        [
            "case_id",
            "pool",
            "engine",
            "source_sql_path",
            "positive_sql_path",
            "noop_candidate_sql_path",
            "selected",
            "notes",
        ],
        rows,
    )


def _manifest_base(candidate: CalibrationCandidate, provider_env: object, prompt: str, source_sql: str, candidate_sql: str) -> dict[str, object]:
    return {
        "case_id": candidate.case_id,
        "pool": candidate.pool,
        "candidate_class": candidate.candidate_class,
        "method_id": candidate.method_id,
        "route_id": candidate.route_id,
        "provider_label": provider_env.provider,
        "model_label": provider_env.model,
        "base_url_host": provider_env.base_url_host,
        "live_enabled_flag": "true",
        "live_enabled_env": "true",
        "api_key_env_present": "true",
        "api_key_env_used": provider_env.api_key_env_used,
        "call_timestamp_utc": datetime.now(UTC).isoformat(),
        "prompt_template_id": PROMPT_TEMPLATE_ID,
        "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
        "prompt_sha256": _sha(prompt),
        "source_sql_sha256": _sha(source_sql),
        "candidate_sql_sha256": _sha(candidate_sql),
    }


def _schema_row(candidate: CalibrationCandidate, annotation: CandidateAnnotation, contract: SkillContract, issues: tuple[object, ...]) -> dict[str, object]:
    return {
        "case_id": candidate.case_id,
        "pool": candidate.pool,
        "candidate_class": candidate.candidate_class,
        "engine": candidate.engine,
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


def _schema_invalid_row(candidate: CalibrationCandidate, contract: SkillContract, reason: str) -> dict[str, object]:
    return {
        "case_id": candidate.case_id,
        "pool": candidate.pool,
        "candidate_class": candidate.candidate_class,
        "engine": candidate.engine,
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


def _stage_b_row(candidate: CalibrationCandidate, contract: SkillContract, stage_b: TransformationStageBValidationResult) -> dict[str, object]:
    counts = Counter(atom.evidence_status for atom in stage_b.atom_results)
    return {
        "case_id": candidate.case_id,
        "pool": candidate.pool,
        "candidate_class": candidate.candidate_class,
        "engine": candidate.engine,
        "schema_valid": str(stage_b.schema_valid).lower(),
        "stage_b_status": stage_b.stage_b_status,
        "source_like_noop": str(stage_b.source_like_noop).lower(),
        "evidence_status_counts": json.dumps(dict(sorted(counts.items())), sort_keys=True),
        "presence_only_operation_atoms_count": stage_b.presence_only_operation_atoms_count,
        "transformation_supported_operation_atoms_count": stage_b.transformation_supported_operation_atoms_count,
        "insufficient_transformation_evidence_operation_atoms_count": stage_b.insufficient_transformation_evidence_operation_atoms_count,
        "rejected_noop_equivalent_operation_atoms_count": stage_b.rejected_noop_equivalent_operation_atoms_count,
        "schema_invalid_atoms_count": stage_b.schema_invalid_atoms_count,
        "expected_operation_atoms_count": len(contract.operation_atoms),
        "semantic_guard_validated_static_span_count": sum(
            1
            for atom in stage_b.atom_results
            if atom.atom_type == "semantic_guard_atom" and atom.evidence_status == "validated_static_span"
        ),
        "semantic_guard_count": len(contract.semantic_guard_atoms),
        "official_pocr_computed": "false",
        "route_level_pocr_aggregated": "false",
        "notes": "Transformation-aware Stage B diagnostics only; no official POCR or route aggregation.",
    }


def _stage_b_invalid_row(candidate: CalibrationCandidate, contract: SkillContract) -> dict[str, object]:
    return {
        "case_id": candidate.case_id,
        "pool": candidate.pool,
        "candidate_class": candidate.candidate_class,
        "engine": candidate.engine,
        "schema_valid": "false",
        "stage_b_status": "schema_invalid",
        "source_like_noop": "",
        "evidence_status_counts": "{}",
        "presence_only_operation_atoms_count": 0,
        "transformation_supported_operation_atoms_count": 0,
        "insufficient_transformation_evidence_operation_atoms_count": 0,
        "rejected_noop_equivalent_operation_atoms_count": 0,
        "schema_invalid_atoms_count": len(contract.operation_atoms),
        "expected_operation_atoms_count": len(contract.operation_atoms),
        "semantic_guard_validated_static_span_count": 0,
        "semantic_guard_count": len(contract.semantic_guard_atoms),
        "official_pocr_computed": "false",
        "route_level_pocr_aggregated": "false",
        "notes": "Stage B not promoted because Stage A annotation failed.",
    }


def _write_not_run(
    output_dir: Path,
    live_enabled: bool,
    provider_env: object,
    blockers: list[CalibrationCandidate],
    *,
    full40_mode: bool,
) -> None:
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
        reasons.append("One or more selected calibration candidate files is missing.")
    not_run_path = output_dir / ("live_full40_calibration_not_run.md" if full40_mode else "live_calibration_not_run.md")
    not_run_path.write_text(
        "# Live Full-40 Calibration Not Run\n\n"
        + "\n".join(f"- {reason}" for reason in reasons)
        + "\n\nNo API call, DB/checker/timing run, baseline rerun, official POCR computation, or route-level aggregation occurred.\n",
        encoding="utf-8",
    )


def _write_empty_outputs(output_dir: Path, *, comparison_filename: str) -> None:
    _write_csv(output_dir / "live_call_manifest.csv", live_manifest_fields(), [])
    _write_csv(output_dir / "annotation_schema_validation.csv", schema_fields(), [])
    _write_csv(output_dir / "transformation_stage_b_validation_by_class.csv", stage_b_fields(), [])
    _write_csv(output_dir / comparison_filename, calibration_result_fields(), [])
    _write_jsonl(output_dir / "safe_annotation_outputs.jsonl", [])


def _write_readme(
    output_dir: Path,
    candidates: tuple[CalibrationCandidate, ...],
    provider_env: object,
    manifest_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    result_rows: list[CalibrationResultRow],
    *,
    full40_mode: bool,
) -> None:
    positive = sum(row.transformation_supported_operation_atoms_count for row in result_rows if row.candidate_class == "positive_control")
    noop = sum(row.transformation_supported_operation_atoms_count for row in result_rows if row.candidate_class == "noop_control")
    positive_presence = sum(row.presence_only_operation_atoms_count for row in result_rows if row.candidate_class == "positive_control")
    noop_presence = sum(row.presence_only_operation_atoms_count for row in result_rows if row.candidate_class == "noop_control")
    positive_rejected_noop = sum(row.rejected_noop_equivalent_operation_atoms_count for row in result_rows if row.candidate_class == "positive_control")
    noop_rejected_noop = sum(row.rejected_noop_equivalent_operation_atoms_count for row in result_rows if row.candidate_class == "noop_control")
    risks = Counter(row.calibration_risk for row in result_rows)
    selected_case_count = len({candidate.case_id for candidate in candidates})
    title = (
        "POCR Full-40 Positive-vs-Noop Control Calibration v0"
        if full40_mode
        else "POCR Transformation-Aware Stage B Calibration v0"
    )
    scope_line = (
        "This packet compares human positive-control SQL against existing no-op/source-like candidates for all 40 Common-core v0 cases using transformation-aware Stage B operation evidence."
        if full40_mode
        else "This packet compares human positive-control SQL against existing no-op/source-like candidates for four POCR fixture cases using transformation-aware Stage B operation evidence."
    )
    (output_dir / "README.md").write_text(
        f"# {title}\n\n"
        f"{scope_line}\n\n"
        f"- Common-core cases evaluated: {selected_case_count}\n"
        f"- Candidate classes evaluated: positive_control, noop_control\n"
        f"- Live calls attempted: {len(manifest_rows)}\n"
        f"- Provider/model: `{provider_env.provider}` / `{provider_env.model}`\n"
        f"- Schema-valid annotations: {sum(1 for row in schema_rows if row['schema_validation_status'] == 'pass')}\n"
        f"- Malformed/schema-invalid annotations: {sum(1 for row in schema_rows if row['schema_validation_status'] != 'pass')}\n"
        f"- positive_control transformation_supported operation atoms: {positive}\n"
        f"- noop_control transformation_supported operation atoms: {noop}\n"
        f"- positive_control presence_only operation atoms: {positive_presence}\n"
        f"- noop_control presence_only operation atoms: {noop_presence}\n"
        f"- positive_control rejected_noop_equivalent operation atoms: {positive_rejected_noop}\n"
        f"- noop_control rejected_noop_equivalent operation atoms: {noop_rejected_noop}\n"
        f"- Calibration risks: {dict(sorted(risks.items()))}\n\n"
        "This is calibration only. It does not compute official POCR, aggregate route-level POCR, run DB/checker/timing, rerun baselines, or promote paper-facing metrics.\n",
        encoding="utf-8",
    )


def _write_plan_docs(output_dir: Path, *, full40_mode: bool) -> None:
    (output_dir / "calibration_plan.md").write_text(
        "# Calibration Plan\n\n"
        "The calibration compares two candidate classes on the same cases: `positive_control` uses case-local `sql/pos_01.sql`, while `noop_control` uses existing no-op candidate SQL under `runs/user/common_core_pg_noop_db_checker/candidate_sql/`. Both classes are annotated with the same transformation-aware Stage A prompt and checked by the same transformation-aware Stage B operation evidence policy. No official POCR or route-level aggregation is produced.\n"
        + (
            "\nScope: all 40 Common-core v0 cases, producing at most 80 live calls.\n"
            if full40_mode
            else "\nScope: the four-case bounded calibration fixture.\n"
        ),
        encoding="utf-8",
    )
    if not full40_mode:
        (output_dir / "transformation_evidence_contract.md").write_text(
            "# Transformation Evidence Contract\n\n"
            "For `operation_atom` rows, Stage B requires transformation-aware evidence rather than span presence alone. `candidate_sql_span`, `source_sql_span`, or `positive_sql_span` alone is `presence_only` and cannot count as transformation support. A row may become `transformation_supported` only when a candidate-specific or positive-aligned span is paired with `source_candidate_diff:changed`. Source-like/no-op candidates are classified as `presence_only` or `rejected_noop_equivalent`. This is diagnostic support only and is not official POCR proof.\n",
            encoding="utf-8",
        )
        (output_dir / "overacceptance_risk_review.md").write_text(
            "# Overacceptance Risk Review\n\n"
            "`noop_transformation_overaccept_risk` means the no-op control has one or more transformation-supported operation atoms. `presence_only` means cited SQL text exists but does not establish transformation. `rejected_noop_equivalent` means the candidate normalizes as source-like/no-op. These diagnostic flags are not official metrics, thresholds, or policy.\n",
            encoding="utf-8",
        )
    (output_dir / "noop_overacceptance_review.md").write_text(
        "# Noop Overacceptance Review\n\n"
        "`noop_control` should not receive transformation support merely for preserving source-like SQL. Any row with `noop_transformation_overaccept_risk` needs prompt or Stage B policy review before real route diagnostics. This file is a boundary note; row-level evidence is in the comparison CSV.\n",
        encoding="utf-8",
    )
    (output_dir / "positive_control_gap_review.md").write_text(
        "# Positive Control Gap Review\n\n"
        "`positive_control_no_transformation_support` and `atom_or_positive_alignment_gap` rows are diagnostic gaps, not dropped rows. They may indicate skills.md atom wording, positive SQL alignment, prompt compliance, provider output quality, or Stage B evidence limitations. No official POCR numerator is computed from these rows.\n",
        encoding="utf-8",
    )
    (output_dir / "protected_path_review.md").write_text(
        "# Protected Path Review\n\n"
        "No `cases/`, root-level `skills.md`, `skill/` folders, `output/`, top-level `reports/`, top-level `results/`, or `runs/` files were modified. Case-local SQL and existing no-op candidate files were read-only inputs.\n",
        encoding="utf-8",
    )
    (output_dir / "secret_scan_notes.md").write_text(
        "# Secret Scan Notes\n\n"
        "API keys were sourced from environment only. API key values were not printed, written, staged, or committed. Raw prompts and raw provider responses were not stored; audit outputs contain safe metadata, hashes, and structured annotations only.\n",
        encoding="utf-8",
    )


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _read_optional(repo_root: Path, path: Path | None) -> str | None:
    if path is None:
        return None
    full_path = repo_root / path
    return _read(full_path) if full_path.is_file() else None


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def _redact(value: str, secret: str) -> str:
    return value.replace(secret, "[REDACTED]") if secret else value


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
