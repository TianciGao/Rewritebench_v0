"""Promotion-diagnostic POCR@planned / POCR@candidate aggregation.

The aggregator consumes durable row-level Stage B metrics CSV files. It emits
diagnostic route summaries only. It does not compute official POCR, promote
paper-facing metrics, update retained evidence, or create leaderboard output.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable

POCR_ROUTE_SUMMARY_FILENAME = "pocr_route_summary.csv"
POCR_ROUTE_SUMMARY_REPORT_FILENAME = "pocr_route_summary.md"

REQUIRED_STAGE_B_ROW_COLUMNS = {
    "run_id",
    "case_set_id",
    "denominator_scope",
    "case_id",
    "pool",
    "engine",
    "method_id",
    "route_id",
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
}

NOT_APPLICABLE_NO_EXPECTED_ATOMS = "not_applicable_no_expected_operation_atoms"
CURATED_MANIFEST_MISSING = "curated_manifest_missing"


@dataclass(frozen=True)
class StageBRowMetric:
    run_id: str
    case_set_id: str
    denominator_scope: str
    case_id: str
    pool: str
    engine: str
    method_id: str
    route_id: str
    planned_pocr_eligible: bool
    candidate_bound: bool
    annotation_status: str
    replay_row_present: bool
    route_mismatch: bool
    candidate_mismatch: bool
    expected_operation_atoms: int
    stage_b_supported_operation_atoms: int
    presence_only_operation_atoms: int
    insufficient_transformation_evidence_atoms: int
    rejected_noop_equivalent_atoms: int
    semantic_guard_atoms: int
    oc_i: Decimal | None
    oc_i_fail_closed: Decimal | None
    pocr_planned_denominator_member: bool
    pocr_candidate_denominator_member: bool
    pocr_curated_denominator_member: bool
    fail_closed_status: str
    not_applicable_reason: str
    diagnostic_only: bool
    official_pocr_computed: bool
    route_level_pocr_aggregated: bool
    paper_metric_promoted: bool
    source_path: Path

    @property
    def not_applicable_no_expected_atoms(self) -> bool:
        return self.not_applicable_reason == NOT_APPLICABLE_NO_EXPECTED_ATOMS

    @property
    def fail_closed(self) -> bool:
        return self.fail_closed_status not in {"", "none", NOT_APPLICABLE_NO_EXPECTED_ATOMS}


@dataclass(frozen=True)
class POCRRouteSummary:
    run_id: str
    case_set_id: str
    denominator_scope: str
    method_id: str
    route_id: str
    engine: str
    planned_pocr_eligible_rows: int
    planned_pocr_numeric_rows: int
    candidate_bound_rows: int
    candidate_pocr_numeric_rows: int
    not_applicable_rows: int
    schema_valid_rows: int
    fail_closed_rows: int
    route_mismatch_rows: int
    candidate_mismatch_rows: int
    no_candidate_rows: int
    annotation_missing_rows: int
    malformed_json_rows: int
    provider_call_failed_rows: int
    timeout_rows: int
    total_expected_operation_atoms: int
    total_stage_b_supported_operation_atoms: int
    total_presence_only_operation_atoms: int
    total_insufficient_transformation_evidence_atoms: int
    total_rejected_noop_equivalent_atoms: int
    total_semantic_guard_atoms: int
    pocr_planned_macro: str
    pocr_candidate_macro: str
    pocr_curated: str
    pocr_curated_status: str
    diagnostic_micro_average_supported_over_expected: str
    macro_formula_used: bool
    official_pocr_computed: bool
    route_level_official_pocr_score_emitted: bool
    paper_metric_promoted: bool
    leaderboard_output: bool
    notes: str


@dataclass(frozen=True)
class POCRAggregateOutputPaths:
    route_summary_csv: Path
    route_summary_report_md: Path | None = None


def read_stage_b_row_metrics(paths: Iterable[Path]) -> tuple[StageBRowMetric, ...]:
    """Read and validate one or more durable Stage B row metrics CSV files."""

    rows: list[StageBRowMetric] = []
    for path in paths:
        rows.extend(_read_one_stage_b_row_metrics_csv(Path(path)))
    return tuple(rows)


def aggregate_pocr_rows(rows: Iterable[StageBRowMetric]) -> tuple[POCRRouteSummary, ...]:
    """Aggregate row metrics into promotion-diagnostic route summaries."""

    grouped: dict[tuple[str, str, str, str, str, str], list[StageBRowMetric]] = defaultdict(list)
    for row in rows:
        _validate_boundary_constants(row)
        grouped[
            (
                row.run_id,
                row.case_set_id,
                row.denominator_scope,
                row.method_id,
                row.route_id,
                row.engine,
            )
        ].append(row)
    return tuple(_summarize_group(key, tuple(group_rows)) for key, group_rows in sorted(grouped.items()))


def write_pocr_route_summary(path: Path, summaries: Iterable[POCRRouteSummary]) -> Path:
    """Write route summaries to `pocr_route_summary.csv`."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=pocr_route_summary_fields(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(pocr_route_summary_csv_rows(summaries))
    return path


def write_pocr_aggregate_outputs(
    *,
    output_root: Path,
    run_id: str,
    summaries: Iterable[POCRRouteSummary],
    write_report: bool = True,
) -> POCRAggregateOutputPaths:
    """Write D035 local diagnostic aggregate outputs for one run id."""

    summary_tuple = tuple(summaries)
    route_summary_csv = output_root / "results" / run_id / "pocr" / "aggregates" / POCR_ROUTE_SUMMARY_FILENAME
    write_pocr_route_summary(route_summary_csv, summary_tuple)
    report_path = None
    if write_report:
        report_path = output_root / "reports" / run_id / POCR_ROUTE_SUMMARY_REPORT_FILENAME
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_pocr_route_summary_report(summary_tuple), encoding="utf-8")
    return POCRAggregateOutputPaths(route_summary_csv=route_summary_csv, route_summary_report_md=report_path)


def pocr_route_summary_fields() -> list[str]:
    return [
        "run_id",
        "case_set_id",
        "denominator_scope",
        "method_id",
        "route_id",
        "engine",
        "planned_pocr_eligible_rows",
        "planned_pocr_numeric_rows",
        "candidate_bound_rows",
        "candidate_pocr_numeric_rows",
        "not_applicable_rows",
        "schema_valid_rows",
        "fail_closed_rows",
        "route_mismatch_rows",
        "candidate_mismatch_rows",
        "no_candidate_rows",
        "annotation_missing_rows",
        "malformed_json_rows",
        "provider_call_failed_rows",
        "timeout_rows",
        "total_expected_operation_atoms",
        "total_stage_b_supported_operation_atoms",
        "total_presence_only_operation_atoms",
        "total_insufficient_transformation_evidence_atoms",
        "total_rejected_noop_equivalent_atoms",
        "total_semantic_guard_atoms",
        "pocr_planned_macro",
        "pocr_candidate_macro",
        "pocr_curated",
        "pocr_curated_status",
        "diagnostic_micro_average_supported_over_expected",
        "macro_formula_used",
        "official_pocr_computed",
        "route_level_official_pocr_score_emitted",
        "paper_metric_promoted",
        "leaderboard_output",
        "notes",
    ]


def pocr_route_summary_csv_rows(summaries: Iterable[POCRRouteSummary]) -> list[dict[str, object]]:
    return [
        {
            "run_id": summary.run_id,
            "case_set_id": summary.case_set_id,
            "denominator_scope": summary.denominator_scope,
            "method_id": summary.method_id,
            "route_id": summary.route_id,
            "engine": summary.engine,
            "planned_pocr_eligible_rows": summary.planned_pocr_eligible_rows,
            "planned_pocr_numeric_rows": summary.planned_pocr_numeric_rows,
            "candidate_bound_rows": summary.candidate_bound_rows,
            "candidate_pocr_numeric_rows": summary.candidate_pocr_numeric_rows,
            "not_applicable_rows": summary.not_applicable_rows,
            "schema_valid_rows": summary.schema_valid_rows,
            "fail_closed_rows": summary.fail_closed_rows,
            "route_mismatch_rows": summary.route_mismatch_rows,
            "candidate_mismatch_rows": summary.candidate_mismatch_rows,
            "no_candidate_rows": summary.no_candidate_rows,
            "annotation_missing_rows": summary.annotation_missing_rows,
            "malformed_json_rows": summary.malformed_json_rows,
            "provider_call_failed_rows": summary.provider_call_failed_rows,
            "timeout_rows": summary.timeout_rows,
            "total_expected_operation_atoms": summary.total_expected_operation_atoms,
            "total_stage_b_supported_operation_atoms": summary.total_stage_b_supported_operation_atoms,
            "total_presence_only_operation_atoms": summary.total_presence_only_operation_atoms,
            "total_insufficient_transformation_evidence_atoms": (
                summary.total_insufficient_transformation_evidence_atoms
            ),
            "total_rejected_noop_equivalent_atoms": summary.total_rejected_noop_equivalent_atoms,
            "total_semantic_guard_atoms": summary.total_semantic_guard_atoms,
            "pocr_planned_macro": summary.pocr_planned_macro,
            "pocr_candidate_macro": summary.pocr_candidate_macro,
            "pocr_curated": summary.pocr_curated,
            "pocr_curated_status": summary.pocr_curated_status,
            "diagnostic_micro_average_supported_over_expected": (
                summary.diagnostic_micro_average_supported_over_expected
            ),
            "macro_formula_used": _bool(summary.macro_formula_used),
            "official_pocr_computed": _bool(summary.official_pocr_computed),
            "route_level_official_pocr_score_emitted": _bool(summary.route_level_official_pocr_score_emitted),
            "paper_metric_promoted": _bool(summary.paper_metric_promoted),
            "leaderboard_output": _bool(summary.leaderboard_output),
            "notes": summary.notes,
        }
        for summary in summaries
    ]


def render_pocr_route_summary_report(summaries: Iterable[POCRRouteSummary]) -> str:
    rows = tuple(summaries)
    lines = [
        "# POCR Route Summary",
        "",
        "This is not official POCR.",
        "",
        "No route-level official POCR score is emitted.",
        "",
        "No paper-facing metric is promoted.",
        "",
        "This aggregator computes promotion-diagnostic POCR@planned and POCR@candidate only.",
        "",
        "POCR@curated remains deferred until a predeclared curated manifest exists.",
        "",
        "Macro-average over per-row OC_i is used.",
        "",
        "Diagnostic micro-average is not the paper formula.",
        "",
        "| route_id | engine | planned_rows | candidate_rows | POCR@planned diagnostic | POCR@candidate diagnostic |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for summary in rows:
        lines.append(
            f"| {summary.route_id} | {summary.engine} | {summary.planned_pocr_numeric_rows} | "
            f"{summary.candidate_pocr_numeric_rows} | {summary.pocr_planned_macro} | {summary.pocr_candidate_macro} |"
        )
    return "\n".join(lines) + "\n"


def _read_one_stage_b_row_metrics_csv(path: Path) -> list[StageBRowMetric]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _validate_required_columns(path, reader.fieldnames)
        return [_metric_from_csv_row(path, row_number, row) for row_number, row in enumerate(reader, start=2)]


def _validate_required_columns(path: Path, fieldnames: list[str] | None) -> None:
    missing = sorted(REQUIRED_STAGE_B_ROW_COLUMNS - set(fieldnames or []))
    if missing:
        raise ValueError(f"{path}: missing required pocr_stage_b_row_metrics.csv columns: {', '.join(missing)}")


def _metric_from_csv_row(path: Path, row_number: int, row: dict[str, str]) -> StageBRowMetric:
    metric = StageBRowMetric(
        run_id=_required(row, "run_id", path, row_number),
        case_set_id=_required(row, "case_set_id", path, row_number),
        denominator_scope=_required(row, "denominator_scope", path, row_number),
        case_id=_required(row, "case_id", path, row_number),
        pool=_required(row, "pool", path, row_number),
        engine=_required(row, "engine", path, row_number),
        method_id=_required(row, "method_id", path, row_number),
        route_id=_required(row, "route_id", path, row_number),
        planned_pocr_eligible=_parse_bool(row, "planned_pocr_eligible", path, row_number),
        candidate_bound=_parse_bool(row, "candidate_bound", path, row_number),
        annotation_status=_required(row, "annotation_status", path, row_number),
        replay_row_present=_parse_bool(row, "replay_row_present", path, row_number),
        route_mismatch=_parse_bool(row, "route_mismatch", path, row_number),
        candidate_mismatch=_parse_bool(row, "candidate_mismatch", path, row_number),
        expected_operation_atoms=_parse_int(row, "expected_operation_atoms", path, row_number),
        stage_b_supported_operation_atoms=_parse_int(row, "stage_b_supported_operation_atoms", path, row_number),
        presence_only_operation_atoms=_parse_int(row, "presence_only_operation_atoms", path, row_number),
        insufficient_transformation_evidence_atoms=_parse_int(
            row,
            "insufficient_transformation_evidence_atoms",
            path,
            row_number,
        ),
        rejected_noop_equivalent_atoms=_parse_int(row, "rejected_noop_equivalent_atoms", path, row_number),
        semantic_guard_atoms=_parse_int(row, "semantic_guard_atoms", path, row_number),
        oc_i=_parse_optional_decimal(row, "oc_i", path, row_number),
        oc_i_fail_closed=_parse_optional_decimal(row, "oc_i_fail_closed", path, row_number),
        pocr_planned_denominator_member=_parse_bool(row, "pocr_planned_denominator_member", path, row_number),
        pocr_candidate_denominator_member=_parse_bool(row, "pocr_candidate_denominator_member", path, row_number),
        pocr_curated_denominator_member=_parse_bool(row, "pocr_curated_denominator_member", path, row_number),
        fail_closed_status=_required(row, "fail_closed_status", path, row_number),
        not_applicable_reason=_required(row, "not_applicable_reason", path, row_number),
        diagnostic_only=_parse_bool(row, "diagnostic_only", path, row_number),
        official_pocr_computed=_parse_bool(row, "official_pocr_computed", path, row_number),
        route_level_pocr_aggregated=_parse_bool(row, "route_level_pocr_aggregated", path, row_number),
        paper_metric_promoted=_parse_bool(row, "paper_metric_promoted", path, row_number),
        source_path=path,
    )
    _validate_boundary_constants(metric)
    return metric


def _summarize_group(
    key: tuple[str, str, str, str, str, str],
    rows: tuple[StageBRowMetric, ...],
) -> POCRRouteSummary:
    run_id, case_set_id, denominator_scope, method_id, route_id, engine = key
    planned_numeric = tuple(_numeric_rows(rows, denominator="planned"))
    candidate_numeric = tuple(_numeric_rows(rows, denominator="candidate"))
    micro_denominator = sum(row.expected_operation_atoms for row in planned_numeric)
    micro_numerator = sum(row.stage_b_supported_operation_atoms for row in planned_numeric)
    notes = (
        "promotion-diagnostic aggregation only; official_pocr_computed=false; "
        "route_level_official_pocr_score_emitted=false; paper_metric_promoted=false; leaderboard_output=false"
    )
    return POCRRouteSummary(
        run_id=run_id,
        case_set_id=case_set_id,
        denominator_scope=denominator_scope,
        method_id=method_id,
        route_id=route_id,
        engine=engine,
        planned_pocr_eligible_rows=sum(1 for row in rows if row.planned_pocr_eligible),
        planned_pocr_numeric_rows=len(planned_numeric),
        candidate_bound_rows=sum(1 for row in rows if row.candidate_bound),
        candidate_pocr_numeric_rows=len(candidate_numeric),
        not_applicable_rows=sum(1 for row in rows if row.not_applicable_no_expected_atoms),
        schema_valid_rows=sum(1 for row in rows if row.annotation_status == "schema_valid"),
        fail_closed_rows=sum(1 for row in rows if row.fail_closed),
        route_mismatch_rows=sum(1 for row in rows if row.route_mismatch or row.fail_closed_status == "route_mismatch"),
        candidate_mismatch_rows=sum(
            1 for row in rows if row.candidate_mismatch or row.fail_closed_status == "candidate_mismatch"
        ),
        no_candidate_rows=sum(1 for row in rows if row.fail_closed_status in _no_candidate_statuses()),
        annotation_missing_rows=sum(
            1 for row in rows if row.annotation_status == "annotation_missing" or row.fail_closed_status == "annotation_missing"
        ),
        malformed_json_rows=sum(
            1 for row in rows if row.annotation_status == "malformed_json" or row.fail_closed_status == "malformed_json"
        ),
        provider_call_failed_rows=sum(
            1
            for row in rows
            if row.annotation_status == "provider_call_failed" or row.fail_closed_status == "provider_call_failed"
        ),
        timeout_rows=sum(1 for row in rows if row.annotation_status == "timeout" or row.fail_closed_status == "timeout"),
        total_expected_operation_atoms=sum(row.expected_operation_atoms for row in rows if row.planned_pocr_eligible),
        total_stage_b_supported_operation_atoms=sum(
            row.stage_b_supported_operation_atoms for row in rows if row.planned_pocr_eligible
        ),
        total_presence_only_operation_atoms=sum(row.presence_only_operation_atoms for row in rows if row.planned_pocr_eligible),
        total_insufficient_transformation_evidence_atoms=sum(
            row.insufficient_transformation_evidence_atoms for row in rows if row.planned_pocr_eligible
        ),
        total_rejected_noop_equivalent_atoms=sum(
            row.rejected_noop_equivalent_atoms for row in rows if row.planned_pocr_eligible
        ),
        total_semantic_guard_atoms=sum(row.semantic_guard_atoms for row in rows if row.planned_pocr_eligible),
        pocr_planned_macro=_mean_oc(planned_numeric),
        pocr_candidate_macro=_mean_oc(candidate_numeric),
        pocr_curated="NA",
        pocr_curated_status=CURATED_MANIFEST_MISSING,
        diagnostic_micro_average_supported_over_expected=(
            _format_decimal(Decimal(micro_numerator) / Decimal(micro_denominator))
            if micro_denominator > 0
            else "NA"
        ),
        macro_formula_used=True,
        official_pocr_computed=False,
        route_level_official_pocr_score_emitted=False,
        paper_metric_promoted=False,
        leaderboard_output=False,
        notes=notes,
    )


def _numeric_rows(rows: tuple[StageBRowMetric, ...], *, denominator: str) -> tuple[StageBRowMetric, ...]:
    if denominator == "planned":
        return tuple(
            row
            for row in rows
            if row.pocr_planned_denominator_member and not row.not_applicable_no_expected_atoms
        )
    if denominator == "candidate":
        return tuple(
            row
            for row in rows
            if row.pocr_candidate_denominator_member and not row.not_applicable_no_expected_atoms
        )
    raise ValueError(f"unknown denominator: {denominator}")


def _mean_oc(rows: tuple[StageBRowMetric, ...]) -> str:
    values = [row.oc_i_fail_closed for row in rows if row.oc_i_fail_closed is not None]
    if not values:
        return "NA"
    return _format_decimal(sum(values, Decimal("0")) / Decimal(len(values)))


def _no_candidate_statuses() -> set[str]:
    return {
        "no_candidate",
        "skipped_no_candidate",
        "missing_candidate",
        "generation_failed",
        "extraction_failed",
    }


def _validate_boundary_constants(row: StageBRowMetric) -> None:
    if not row.diagnostic_only:
        raise ValueError(f"{row.source_path}: diagnostic_only must be true for {row.case_id}")
    if row.official_pocr_computed:
        raise ValueError(f"{row.source_path}: official_pocr_computed must be false for {row.case_id}")
    if row.route_level_pocr_aggregated:
        raise ValueError(f"{row.source_path}: route_level_pocr_aggregated must be false for {row.case_id}")
    if row.paper_metric_promoted:
        raise ValueError(f"{row.source_path}: paper_metric_promoted must be false for {row.case_id}")


def _required(row: dict[str, str], field: str, path: Path, row_number: int) -> str:
    value = row.get(field, "")
    if value == "":
        raise ValueError(f"{path}:{row_number}: required field {field!r} is empty")
    return value


def _parse_bool(row: dict[str, str], field: str, path: Path, row_number: int) -> bool:
    value = _required(row, field, path, row_number).strip().lower()
    if value == "true":
        return True
    if value == "false":
        return False
    raise ValueError(f"{path}:{row_number}: field {field!r} must be true or false, got {value!r}")


def _parse_int(row: dict[str, str], field: str, path: Path, row_number: int) -> int:
    value = _required(row, field, path, row_number)
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"{path}:{row_number}: field {field!r} must be an integer, got {value!r}") from exc
    if parsed < 0:
        raise ValueError(f"{path}:{row_number}: field {field!r} must be non-negative")
    return parsed


def _parse_optional_decimal(row: dict[str, str], field: str, path: Path, row_number: int) -> Decimal | None:
    value = row.get(field, "").strip()
    if value in {"", "NA"}:
        return None
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{path}:{row_number}: field {field!r} must be decimal or NA, got {value!r}") from exc


def _format_decimal(value: Decimal) -> str:
    return format(value.quantize(Decimal("0.000000000001")), "f")


def _bool(value: bool) -> str:
    return str(value).lower()
