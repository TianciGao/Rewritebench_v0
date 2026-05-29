"""Durable row-level POCR Stage B metrics export.

This module writes diagnostic aggregator-input rows only. It does not compute
official POCR, aggregate route-level POCR, promote paper metrics, or create
leaderboard output.
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from sql_rewrite_bench.pocr.diagnostic_output_schema import POCRDiagnosticRow

STAGE_B_ROW_METRICS_FILENAME = "pocr_stage_b_row_metrics.csv"
DEFAULT_CASE_SET_ID = "common_core_v0"


def stage_b_row_metric_fields() -> list[str]:
    """Return the stable minimal row-level Stage B metrics CSV columns."""

    return [
        "run_id",
        "case_set_id",
        "denominator_scope",
        "case_id",
        "pool",
        "engine",
        "method_id",
        "route_id",
        "candidate_sha256",
        "planned_pocr_eligible",
        "candidate_bound",
        "annotation_status",
        "replay_row_present",
        "route_mismatch",
        "candidate_mismatch",
        "expected_operation_atoms",
        "stage_b_supported_operation_atoms",
        "presence_only_operation_atoms",
        "insufficient_transformation_evidence_atoms",
        "rejected_noop_equivalent_atoms",
        "semantic_guard_atoms",
        "oc_i",
        "oc_i_fail_closed",
        "pocr_planned_denominator_member",
        "pocr_candidate_denominator_member",
        "pocr_curated_denominator_member",
        "fail_closed_status",
        "not_applicable_reason",
        "diagnostic_only",
        "official_pocr_computed",
        "route_level_pocr_aggregated",
        "paper_metric_promoted",
        "notes",
    ]


def export_stage_b_row_metrics(
    path: Path,
    rows: tuple[POCRDiagnosticRow, ...],
    *,
    repo_root: Path | None = None,
    case_set_id: str = DEFAULT_CASE_SET_ID,
    denominator_scope: str | None = None,
) -> Path:
    """Write one durable row-level POCR Stage B metrics CSV.

    The output is an input artifact for future aggregation. It intentionally
    does not emit POCR@planned, POCR@candidate, POCR@curated, or any route-level
    score.
    """

    scope = denominator_scope or _infer_denominator_scope(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=stage_b_row_metric_fields(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(
            stage_b_row_metric_csv_rows(
                rows,
                repo_root=repo_root,
                case_set_id=case_set_id,
                denominator_scope=scope,
            )
        )
    return path


def stage_b_row_metric_csv_rows(
    rows: tuple[POCRDiagnosticRow, ...],
    *,
    repo_root: Path | None = None,
    case_set_id: str = DEFAULT_CASE_SET_ID,
    denominator_scope: str | None = None,
) -> list[dict[str, object]]:
    """Convert diagnostic rows to durable row-level Stage B metric rows."""

    scope = denominator_scope or _infer_denominator_scope(rows)
    return [
        _row_to_metric_csv_row(row, repo_root=repo_root, case_set_id=case_set_id, denominator_scope=scope)
        for row in rows
    ]


def _row_to_metric_csv_row(
    row: POCRDiagnosticRow,
    *,
    repo_root: Path | None,
    case_set_id: str,
    denominator_scope: str,
) -> dict[str, object]:
    expected = row.expected_operation_atoms_count
    supported = row.transformation_supported_operation_atoms_count
    route_mismatch = _has_status(row, "route_mismatch")
    candidate_mismatch = _has_status(row, "candidate_mismatch")
    candidate_sha256 = _candidate_sha256(row, repo_root=repo_root)
    candidate_bound = row.candidate_present and bool(candidate_sha256)
    not_applicable_reason = "not_applicable_no_expected_operation_atoms" if expected == 0 else "none"
    fail_closed_status = _fail_closed_status(
        row,
        route_mismatch=route_mismatch,
        candidate_mismatch=candidate_mismatch,
        not_applicable_reason=not_applicable_reason,
    )
    fail_closed = fail_closed_status not in {"none", "not_applicable_no_expected_operation_atoms"}
    planned_member = expected > 0
    candidate_member = candidate_bound and expected > 0
    oc_i = _oc_i(supported=supported, expected=expected, fail_closed=fail_closed)
    oc_i_fail_closed = _oc_i_fail_closed(
        supported=supported,
        expected=expected,
        fail_closed=fail_closed,
        denominator_member=planned_member or candidate_member,
    )

    return {
        "run_id": row.run_id,
        "case_set_id": case_set_id,
        "denominator_scope": denominator_scope,
        "case_id": row.case_id,
        "pool": row.pool,
        "engine": row.engine,
        "method_id": row.method_id,
        "route_id": row.route_id,
        "candidate_sha256": candidate_sha256,
        "planned_pocr_eligible": _bool(True),
        "candidate_bound": _bool(candidate_bound),
        "annotation_status": row.annotation_status,
        "replay_row_present": _bool(True),
        "route_mismatch": _bool(route_mismatch),
        "candidate_mismatch": _bool(candidate_mismatch),
        "expected_operation_atoms": expected,
        "stage_b_supported_operation_atoms": supported,
        "presence_only_operation_atoms": row.presence_only_operation_atoms_count,
        "insufficient_transformation_evidence_atoms": row.insufficient_transformation_evidence_operation_atoms_count,
        "rejected_noop_equivalent_atoms": row.rejected_noop_equivalent_operation_atoms_count,
        "semantic_guard_atoms": row.semantic_guard_atoms_count,
        "oc_i": oc_i,
        "oc_i_fail_closed": oc_i_fail_closed,
        "pocr_planned_denominator_member": _bool(planned_member),
        "pocr_candidate_denominator_member": _bool(candidate_member),
        "pocr_curated_denominator_member": _bool(False),
        "fail_closed_status": fail_closed_status,
        "not_applicable_reason": not_applicable_reason,
        "diagnostic_only": _bool(row.diagnostic_only),
        "official_pocr_computed": _bool(row.official_pocr_computed),
        "route_level_pocr_aggregated": _bool(row.route_level_pocr_aggregated),
        "paper_metric_promoted": _bool(row.paper_metric_promoted),
        "notes": row.boundary_notes,
    }


def _candidate_sha256(row: POCRDiagnosticRow, *, repo_root: Path | None) -> str:
    if not row.candidate_present or not row.candidate_path:
        return ""
    candidate_path = Path(row.candidate_path)
    if not candidate_path.is_absolute() and repo_root is not None:
        candidate_path = repo_root / candidate_path
    if not candidate_path.is_file():
        return ""
    digest = hashlib.sha256()
    with candidate_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _fail_closed_status(
    row: POCRDiagnosticRow,
    *,
    route_mismatch: bool,
    candidate_mismatch: bool,
    not_applicable_reason: str,
) -> str:
    if not_applicable_reason != "none":
        return not_applicable_reason
    if route_mismatch:
        return "route_mismatch"
    if candidate_mismatch:
        return "candidate_mismatch"
    if not row.candidate_present or row.stage_b_status == "missing_candidate":
        return "skipped_no_candidate"
    if _has_status(row, "malformed_json"):
        return "malformed_json"
    if _has_status(row, "provider_call_failed"):
        return "provider_call_failed"
    if _has_status(row, "timeout"):
        return "timeout"
    if row.annotation_status == "annotation_missing" or row.stage_b_status == "annotation_missing":
        return "annotation_missing"
    if row.annotation_status == "schema_invalid" or row.stage_b_status == "schema_invalid":
        return "schema_invalid"
    if not row.skill_present:
        return "schema_invalid"
    return "none"


def _has_status(row: POCRDiagnosticRow, needle: str) -> bool:
    text = " ".join([row.annotation_status, row.stage_b_status, row.boundary_notes]).lower()
    return needle.lower() in text


def _oc_i(*, supported: int, expected: int, fail_closed: bool) -> str:
    if expected == 0:
        return "NA"
    if fail_closed:
        return ""
    return _format_ratio(supported, expected)


def _oc_i_fail_closed(*, supported: int, expected: int, fail_closed: bool, denominator_member: bool) -> str:
    if expected == 0:
        return "NA"
    if fail_closed and denominator_member:
        return "0"
    return _format_ratio(supported, expected)


def _format_ratio(numerator: int, denominator: int) -> str:
    return f"{numerator / denominator:.12f}"


def _infer_denominator_scope(rows: tuple[POCRDiagnosticRow, ...]) -> str:
    engines = {row.engine for row in rows}
    if engines == {"postgres"}:
        return "pg40_postgres_only"
    if len(engines) == 1:
        return f"common_core_v0_{next(iter(engines))}_only"
    return "custom"


def _bool(value: bool) -> str:
    return str(value).lower()
