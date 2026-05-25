"""Diagnostic POCR user-output schema.

These objects describe diagnostic support output only. They do not compute
official Positive Operation Coverage Rate, route-level POCR, paper metrics, or
leaderboard rows.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

POOL_ORDER = ("PERF", "CONS", "PORT", "LONGTAIL")


@dataclass(frozen=True)
class POCRDiagnosticRow:
    run_id: str
    case_id: str
    pool: str
    engine: str
    method_id: str
    route_id: str
    candidate_path: str
    candidate_present: bool
    skill_present: bool
    annotation_status: str
    stage_b_status: str
    expected_operation_atoms_count: int
    stage_a_implemented_operation_atoms_count: int
    transformation_supported_operation_atoms_count: int
    presence_only_operation_atoms_count: int
    insufficient_transformation_evidence_operation_atoms_count: int
    rejected_noop_equivalent_operation_atoms_count: int
    schema_invalid_atoms_count: int
    semantic_guard_atoms_count: int
    diagnostic_only: bool = True
    official_pocr_computed: bool = False
    route_level_pocr_aggregated: bool = False
    paper_metric_promoted: bool = False
    boundary_notes: str = "Positive Operation Coverage diagnostic support only; not official POCR"

    def __post_init__(self) -> None:
        if not self.diagnostic_only:
            raise ValueError("diagnostic_only must be true for POCR diagnostic output")
        if self.official_pocr_computed:
            raise ValueError("official_pocr_computed must be false for POCR diagnostic output")
        if self.route_level_pocr_aggregated:
            raise ValueError("route_level_pocr_aggregated must be false for POCR diagnostic output")
        if self.paper_metric_promoted:
            raise ValueError("paper_metric_promoted must be false for POCR diagnostic output")


@dataclass(frozen=True)
class POCRDiagnosticPoolSummary:
    pool: str
    rows_resolved: int
    schema_valid_annotations: int
    malformed_or_schema_invalid_annotations: int
    expected_operation_atoms: int
    transformation_supported_operation_atoms: int
    presence_only_operation_atoms: int
    insufficient_transformation_evidence_operation_atoms: int
    rejected_noop_equivalent_operation_atoms: int
    diagnostic_only: bool = True
    official_pocr_computed: bool = False


def diagnostic_row_fields() -> list[str]:
    return [
        "run_id",
        "case_id",
        "pool",
        "engine",
        "method_id",
        "route_id",
        "candidate_path",
        "candidate_present",
        "skill_present",
        "annotation_status",
        "stage_b_status",
        "expected_operation_atoms_count",
        "stage_a_implemented_operation_atoms_count",
        "transformation_supported_operation_atoms_count",
        "presence_only_operation_atoms_count",
        "insufficient_transformation_evidence_operation_atoms_count",
        "rejected_noop_equivalent_operation_atoms_count",
        "schema_invalid_atoms_count",
        "semantic_guard_atoms_count",
        "diagnostic_only",
        "official_pocr_computed",
        "route_level_pocr_aggregated",
        "paper_metric_promoted",
        "boundary_notes",
    ]


def diagnostic_summary_fields() -> list[str]:
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


def diagnostic_rows_to_csv_rows(rows: tuple[POCRDiagnosticRow, ...]) -> list[dict[str, object]]:
    return [
        {
            "run_id": row.run_id,
            "case_id": row.case_id,
            "pool": row.pool,
            "engine": row.engine,
            "method_id": row.method_id,
            "route_id": row.route_id,
            "candidate_path": row.candidate_path,
            "candidate_present": _bool(row.candidate_present),
            "skill_present": _bool(row.skill_present),
            "annotation_status": row.annotation_status,
            "stage_b_status": row.stage_b_status,
            "expected_operation_atoms_count": row.expected_operation_atoms_count,
            "stage_a_implemented_operation_atoms_count": row.stage_a_implemented_operation_atoms_count,
            "transformation_supported_operation_atoms_count": row.transformation_supported_operation_atoms_count,
            "presence_only_operation_atoms_count": row.presence_only_operation_atoms_count,
            "insufficient_transformation_evidence_operation_atoms_count": row.insufficient_transformation_evidence_operation_atoms_count,
            "rejected_noop_equivalent_operation_atoms_count": row.rejected_noop_equivalent_operation_atoms_count,
            "schema_invalid_atoms_count": row.schema_invalid_atoms_count,
            "semantic_guard_atoms_count": row.semantic_guard_atoms_count,
            "diagnostic_only": _bool(row.diagnostic_only),
            "official_pocr_computed": _bool(row.official_pocr_computed),
            "route_level_pocr_aggregated": _bool(row.route_level_pocr_aggregated),
            "paper_metric_promoted": _bool(row.paper_metric_promoted),
            "boundary_notes": row.boundary_notes,
        }
        for row in rows
    ]


def diagnostic_summaries_to_csv_rows(summaries: tuple[POCRDiagnosticPoolSummary, ...]) -> list[dict[str, object]]:
    return [
        {
            "pool": summary.pool,
            "rows_resolved": summary.rows_resolved,
            "schema_valid_annotations": summary.schema_valid_annotations,
            "malformed_or_schema_invalid_annotations": summary.malformed_or_schema_invalid_annotations,
            "expected_operation_atoms": summary.expected_operation_atoms,
            "transformation_supported_operation_atoms": summary.transformation_supported_operation_atoms,
            "presence_only_operation_atoms": summary.presence_only_operation_atoms,
            "insufficient_transformation_evidence_operation_atoms": summary.insufficient_transformation_evidence_operation_atoms,
            "rejected_noop_equivalent_operation_atoms": summary.rejected_noop_equivalent_operation_atoms,
            "diagnostic_only": _bool(summary.diagnostic_only),
            "official_pocr_computed": _bool(summary.official_pocr_computed),
        }
        for summary in summaries
    ]


def summarize_by_pool(rows: tuple[POCRDiagnosticRow, ...]) -> tuple[POCRDiagnosticPoolSummary, ...]:
    by_pool: dict[str, list[POCRDiagnosticRow]] = defaultdict(list)
    for row in rows:
        by_pool[row.pool].append(row)
    summaries: list[POCRDiagnosticPoolSummary] = []
    for pool in POOL_ORDER:
        pool_rows = by_pool.get(pool, [])
        summaries.append(
            POCRDiagnosticPoolSummary(
                pool=pool,
                rows_resolved=len(pool_rows),
                schema_valid_annotations=sum(1 for row in pool_rows if row.annotation_status == "schema_valid"),
                malformed_or_schema_invalid_annotations=sum(1 for row in pool_rows if row.annotation_status == "schema_invalid"),
                expected_operation_atoms=sum(row.expected_operation_atoms_count for row in pool_rows),
                transformation_supported_operation_atoms=sum(
                    row.transformation_supported_operation_atoms_count for row in pool_rows
                ),
                presence_only_operation_atoms=sum(row.presence_only_operation_atoms_count for row in pool_rows),
                insufficient_transformation_evidence_operation_atoms=sum(
                    row.insufficient_transformation_evidence_operation_atoms_count for row in pool_rows
                ),
                rejected_noop_equivalent_operation_atoms=sum(
                    row.rejected_noop_equivalent_operation_atoms_count for row in pool_rows
                ),
            )
        )
    return tuple(summaries)


def render_diagnostic_markdown_report(
    *,
    run_id: str,
    rows: tuple[POCRDiagnosticRow, ...],
    summaries: tuple[POCRDiagnosticPoolSummary, ...],
) -> str:
    total_rows = len(rows)
    schema_valid = sum(summary.schema_valid_annotations for summary in summaries)
    schema_invalid = sum(summary.malformed_or_schema_invalid_annotations for summary in summaries)
    transformation_supported = sum(summary.transformation_supported_operation_atoms for summary in summaries)
    presence_only = sum(summary.presence_only_operation_atoms for summary in summaries)
    insufficient = sum(summary.insufficient_transformation_evidence_operation_atoms for summary in summaries)
    rejected_noop = sum(summary.rejected_noop_equivalent_operation_atoms for summary in summaries)
    lines = [
        "# POCR Diagnostic Report",
        "",
        "Positive Operation Coverage diagnostic support.",
        "",
        f"- run_id: `{run_id}`",
        f"- rows resolved: {total_rows}",
        f"- schema-valid annotations: {schema_valid}",
        f"- malformed/schema-invalid annotations: {schema_invalid}",
        f"- transformation-supported operation atoms: {transformation_supported}",
        f"- presence-only operation atoms: {presence_only}",
        f"- insufficient-transformation-evidence operation atoms: {insufficient}",
        f"- rejected-noop-equivalent operation atoms: {rejected_noop}",
        "",
        "This is not official POCR.",
        "",
        "Stage A annotation alone is not counted.",
        "",
        "Stage B transformation-aware validation is diagnostic only.",
        "",
        "Semantic guard atoms are not part of operation coverage numerator.",
        "",
        "No route-level POCR score is emitted.",
        "",
        "No paper metric is promoted and no leaderboard row is created.",
        "",
        "## Summary By Pool",
        "",
        "| pool | rows_resolved | schema_valid_annotations | transformation_supported_operation_atoms | presence_only_operation_atoms | insufficient_transformation_evidence_operation_atoms | rejected_noop_equivalent_operation_atoms |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for summary in summaries:
        lines.append(
            f"| {summary.pool} | {summary.rows_resolved} | {summary.schema_valid_annotations} | "
            f"{summary.transformation_supported_operation_atoms} | {summary.presence_only_operation_atoms} | "
            f"{summary.insufficient_transformation_evidence_operation_atoms} | {summary.rejected_noop_equivalent_operation_atoms} |"
        )
    return "\n".join(lines) + "\n"


def write_diagnostic_rows_csv(path: Path, rows: tuple[POCRDiagnosticRow, ...]) -> None:
    _write_csv(path, diagnostic_row_fields(), diagnostic_rows_to_csv_rows(rows))


def write_diagnostic_summary_csv(path: Path, summaries: tuple[POCRDiagnosticPoolSummary, ...]) -> None:
    _write_csv(path, diagnostic_summary_fields(), diagnostic_summaries_to_csv_rows(summaries))


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _bool(value: bool) -> str:
    return str(value).lower()
