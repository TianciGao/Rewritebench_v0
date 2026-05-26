import csv
from pathlib import Path

import pytest

from sql_rewrite_bench.pocr.pocr_aggregator import (
    aggregate_pocr_rows,
    pocr_route_summary_fields,
    read_stage_b_row_metrics,
    write_pocr_aggregate_outputs,
    write_pocr_route_summary,
)
from sql_rewrite_bench.pocr.stage_b_row_metrics import stage_b_row_metric_fields


def _row(
    case_id: str,
    *,
    expected: int = 2,
    supported: int = 1,
    oc: str | None = None,
    planned_member: bool = True,
    candidate_bound: bool = True,
    candidate_member: bool = True,
    annotation_status: str = "schema_valid",
    fail_closed_status: str = "none",
    not_applicable_reason: str = "none",
    route_mismatch: bool = False,
    candidate_mismatch: bool = False,
    presence_only: int = 0,
    insufficient: int = 0,
    rejected_noop: int = 0,
    semantic_guard: int = 1,
    method_id: str = "method",
    route_id: str = "route",
) -> dict[str, object]:
    value = f"{supported / expected:.12f}" if oc is None and expected > 0 and fail_closed_status == "none" else oc
    if expected == 0:
        value = "NA"
        not_applicable_reason = "not_applicable_no_expected_operation_atoms"
        planned_member = False
        candidate_member = False
        fail_closed_status = "not_applicable_no_expected_operation_atoms"
    if fail_closed_status not in {"none", "not_applicable_no_expected_operation_atoms"}:
        value = ""
    oc_fail_closed = "NA" if expected == 0 else ("0" if fail_closed_status != "none" else value)
    return {
        "run_id": "aggregate_test",
        "case_set_id": "common_core_v0",
        "denominator_scope": "pg40_postgres_only",
        "case_id": case_id,
        "pool": case_id.split("_", maxsplit=1)[0],
        "engine": "postgres",
        "method_id": method_id,
        "route_id": route_id,
        "candidate_sha256": "a" * 64 if candidate_bound else "",
        "planned_pocr_eligible": "true",
        "candidate_bound": str(candidate_bound).lower(),
        "annotation_status": annotation_status,
        "replay_row_present": "true",
        "route_mismatch": str(route_mismatch).lower(),
        "candidate_mismatch": str(candidate_mismatch).lower(),
        "expected_operation_atoms": expected,
        "stage_b_supported_operation_atoms": supported,
        "presence_only_operation_atoms": presence_only,
        "insufficient_transformation_evidence_atoms": insufficient,
        "rejected_noop_equivalent_atoms": rejected_noop,
        "semantic_guard_atoms": semantic_guard,
        "oc_i": value or "",
        "oc_i_fail_closed": oc_fail_closed,
        "pocr_planned_denominator_member": str(planned_member).lower(),
        "pocr_candidate_denominator_member": str(candidate_member).lower(),
        "pocr_curated_denominator_member": "false",
        "fail_closed_status": fail_closed_status,
        "not_applicable_reason": not_applicable_reason,
        "diagnostic_only": "true",
        "official_pocr_computed": "false",
        "route_level_pocr_aggregated": "false",
        "paper_metric_promoted": "false",
        "notes": "fixture diagnostic row",
    }


def _write_metrics(path: Path, rows: list[dict[str, object]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=stage_b_row_metric_fields(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return path


def _summary(tmp_path: Path, rows: list[dict[str, object]]):
    path = _write_metrics(tmp_path / "pocr_stage_b_row_metrics.csv", rows)
    [summary] = aggregate_pocr_rows(read_stage_b_row_metrics([path]))
    return summary


def test_aggregates_two_normal_rows_and_computes_macro_average(tmp_path: Path) -> None:
    summary = _summary(
        tmp_path,
        [
            _row("PERF_0006", expected=2, supported=1),
            _row("PERF_0007", expected=4, supported=4),
        ],
    )

    assert summary.planned_pocr_numeric_rows == 2
    assert summary.candidate_pocr_numeric_rows == 2
    assert summary.pocr_planned_macro == "0.750000000000"
    assert summary.pocr_candidate_macro == "0.750000000000"


def test_macro_average_is_distinct_from_diagnostic_micro_average(tmp_path: Path) -> None:
    summary = _summary(
        tmp_path,
        [
            _row("PERF_0006", expected=1, supported=1),
            _row("PERF_0007", expected=9, supported=0),
        ],
    )

    assert summary.pocr_planned_macro == "0.500000000000"
    assert summary.diagnostic_micro_average_supported_over_expected == "0.100000000000"


def test_planned_includes_fail_closed_rows_with_zero_oc(tmp_path: Path) -> None:
    summary = _summary(
        tmp_path,
        [
            _row("PERF_0006", expected=2, supported=2),
            _row("PERF_0007", expected=2, supported=0, annotation_status="malformed_json", fail_closed_status="malformed_json"),
        ],
    )

    assert summary.planned_pocr_numeric_rows == 2
    assert summary.fail_closed_rows == 1
    assert summary.malformed_json_rows == 1
    assert summary.pocr_planned_macro == "0.500000000000"


def test_candidate_excludes_no_candidate_but_includes_candidate_bound_fail_closed(tmp_path: Path) -> None:
    summary = _summary(
        tmp_path,
        [
            _row("PERF_0006", expected=2, supported=2),
            _row(
                "PERF_0007",
                expected=2,
                supported=0,
                candidate_bound=False,
                candidate_member=False,
                annotation_status="annotation_missing",
                fail_closed_status="skipped_no_candidate",
            ),
            _row(
                "PERF_0008",
                expected=2,
                supported=0,
                annotation_status="provider_call_failed",
                fail_closed_status="provider_call_failed",
            ),
        ],
    )

    assert summary.planned_pocr_numeric_rows == 3
    assert summary.candidate_bound_rows == 2
    assert summary.candidate_pocr_numeric_rows == 2
    assert summary.no_candidate_rows == 1
    assert summary.provider_call_failed_rows == 1
    assert summary.pocr_planned_macro == "0.333333333333"
    assert summary.pocr_candidate_macro == "0.500000000000"


def test_no_expected_operation_atoms_are_counted_not_applicable_and_excluded(tmp_path: Path) -> None:
    summary = _summary(
        tmp_path,
        [
            _row("PERF_0006", expected=2, supported=2),
            _row("CONS_0005", expected=0, supported=0),
        ],
    )

    assert summary.not_applicable_rows == 1
    assert summary.planned_pocr_eligible_rows == 2
    assert summary.planned_pocr_numeric_rows == 1
    assert summary.candidate_pocr_numeric_rows == 1
    assert summary.pocr_planned_macro == "1.000000000000"


def test_curated_is_always_na_and_boundary_constants_hold(tmp_path: Path) -> None:
    summary = _summary(tmp_path, [_row("PERF_0006", expected=2, supported=1)])

    assert summary.pocr_curated == "NA"
    assert summary.pocr_curated_status == "curated_manifest_missing"
    assert summary.macro_formula_used is True
    assert summary.official_pocr_computed is False
    assert summary.route_level_official_pocr_score_emitted is False
    assert summary.paper_metric_promoted is False
    assert summary.leaderboard_output is False


def test_missing_required_input_column_fails_closed_with_clear_error(tmp_path: Path) -> None:
    path = tmp_path / "pocr_stage_b_row_metrics.csv"
    row = _row("PERF_0006")
    row.pop("oc_i_fail_closed")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[field for field in stage_b_row_metric_fields() if field != "oc_i_fail_closed"])
        writer.writeheader()
        writer.writerow(row)

    with pytest.raises(ValueError, match="missing required pocr_stage_b_row_metrics.csv columns: oc_i_fail_closed"):
        read_stage_b_row_metrics([path])


def test_route_and_candidate_mismatch_rows_are_counted(tmp_path: Path) -> None:
    summary = _summary(
        tmp_path,
        [
            _row(
                "PERF_0006",
                expected=2,
                supported=0,
                annotation_status="schema_invalid",
                fail_closed_status="route_mismatch",
                route_mismatch=True,
            ),
            _row(
                "PERF_0007",
                expected=2,
                supported=0,
                annotation_status="schema_invalid",
                fail_closed_status="candidate_mismatch",
                candidate_mismatch=True,
            ),
        ],
    )

    assert summary.route_mismatch_rows == 1
    assert summary.candidate_mismatch_rows == 1
    assert summary.fail_closed_rows == 2
    assert summary.pocr_planned_macro == "0.000000000000"


def test_noop_all_zero_route_aggregates_to_zero(tmp_path: Path) -> None:
    summary = _summary(
        tmp_path,
        [
            _row("CONS_0005", expected=3, supported=0, route_id="sqlglot_noop_pg40_pocr_sanity_control"),
            _row("CONS_0007", expected=3, supported=0, route_id="sqlglot_noop_pg40_pocr_sanity_control"),
        ],
    )

    assert summary.route_id == "sqlglot_noop_pg40_pocr_sanity_control"
    assert summary.pocr_planned_macro == "0.000000000000"
    assert summary.pocr_candidate_macro == "0.000000000000"


def test_writes_route_summary_csv_with_required_columns(tmp_path: Path) -> None:
    summary = _summary(tmp_path, [_row("PERF_0006", expected=2, supported=1)])
    output_path = tmp_path / "results" / "aggregate_test" / "pocr" / "aggregates" / "pocr_route_summary.csv"

    write_pocr_route_summary(output_path, (summary,))

    with output_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1
    assert set(pocr_route_summary_fields()).issubset(rows[0])
    assert rows[0]["pocr_curated"] == "NA"
    assert rows[0]["official_pocr_computed"] == "false"
    assert rows[0]["leaderboard_output"] == "false"


def test_writes_d035_aggregate_outputs_and_report(tmp_path: Path) -> None:
    summary = _summary(tmp_path, [_row("PERF_0006", expected=2, supported=1)])

    paths = write_pocr_aggregate_outputs(output_root=tmp_path / "output", run_id="aggregate_test", summaries=(summary,))

    assert paths.route_summary_csv.as_posix().endswith(
        "output/results/aggregate_test/pocr/aggregates/pocr_route_summary.csv"
    )
    assert paths.route_summary_report_md is not None
    assert paths.route_summary_report_md.as_posix().endswith("output/reports/aggregate_test/pocr_route_summary.md")
    report = paths.route_summary_report_md.read_text(encoding="utf-8")
    assert "This aggregator computes promotion-diagnostic POCR@planned and POCR@candidate only." in report
