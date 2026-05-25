import pytest

from sql_rewrite_bench.pocr.diagnostic_output_schema import (
    POCRDiagnosticRow,
    diagnostic_row_fields,
    diagnostic_rows_to_csv_rows,
    render_diagnostic_markdown_report,
    summarize_by_pool,
)


def _row(pool: str = "PERF") -> POCRDiagnosticRow:
    return POCRDiagnosticRow(
        run_id="pocr_contract_test",
        case_id="PERF_0006" if pool == "PERF" else "CONS_0005",
        pool=pool,
        engine="postgres",
        method_id="direct_llm_original",
        route_id="direct_llm_original_pg40_pocr_diagnostic",
        candidate_path="runs/user/example/candidate_sql/PERF_0006__postgres.sql",
        candidate_present=True,
        skill_present=True,
        annotation_status="schema_valid",
        stage_b_status="transformation_evidence_partial",
        expected_operation_atoms_count=2,
        stage_a_implemented_operation_atoms_count=1,
        transformation_supported_operation_atoms_count=1,
        presence_only_operation_atoms_count=0,
        insufficient_transformation_evidence_operation_atoms_count=1,
        rejected_noop_equivalent_operation_atoms_count=0,
        schema_invalid_atoms_count=0,
        semantic_guard_atoms_count=2,
    )


def test_diagnostic_row_schema_serializes_required_boundaries() -> None:
    row = _row()

    csv_row = diagnostic_rows_to_csv_rows((row,))[0]

    assert list(csv_row) == diagnostic_row_fields()
    assert csv_row["diagnostic_only"] == "true"
    assert csv_row["official_pocr_computed"] == "false"
    assert csv_row["route_level_pocr_aggregated"] == "false"
    assert csv_row["paper_metric_promoted"] == "false"
    assert row.semantic_guard_atoms_count == 2
    assert row.transformation_supported_operation_atoms_count == 1


def test_diagnostic_row_rejects_metric_promotion_flags() -> None:
    with pytest.raises(ValueError, match="official_pocr_computed"):
        POCRDiagnosticRow(
            run_id="bad",
            case_id="PERF_0006",
            pool="PERF",
            engine="postgres",
            method_id="m",
            route_id="r",
            candidate_path="candidate.sql",
            candidate_present=True,
            skill_present=True,
            annotation_status="schema_valid",
            stage_b_status="diagnostic",
            expected_operation_atoms_count=1,
            stage_a_implemented_operation_atoms_count=1,
            transformation_supported_operation_atoms_count=1,
            presence_only_operation_atoms_count=0,
            insufficient_transformation_evidence_operation_atoms_count=0,
            rejected_noop_equivalent_operation_atoms_count=0,
            schema_invalid_atoms_count=0,
            semantic_guard_atoms_count=1,
            official_pocr_computed=True,
        )


def test_summary_by_pool_is_diagnostic_counts_not_route_level_pocr() -> None:
    summaries = summarize_by_pool((_row("PERF"), _row("CONS")))

    by_pool = {summary.pool: summary for summary in summaries}
    assert by_pool["PERF"].rows_resolved == 1
    assert by_pool["CONS"].rows_resolved == 1
    assert by_pool["PORT"].rows_resolved == 0
    assert all(summary.diagnostic_only is True for summary in summaries)
    assert all(summary.official_pocr_computed is False for summary in summaries)


def test_markdown_report_includes_required_boundary_wording() -> None:
    rows = (_row(),)
    summaries = summarize_by_pool(rows)

    report = render_diagnostic_markdown_report(run_id="pocr_contract_test", rows=rows, summaries=summaries)

    assert "Positive Operation Coverage diagnostic support" in report
    assert "This is not official POCR." in report
    assert "Stage A annotation alone is not counted." in report
    assert "Stage B transformation-aware validation is diagnostic only." in report
    assert "Semantic guard atoms are not part of operation coverage numerator." in report
    assert "No route-level POCR score is emitted." in report
    assert "No paper metric is promoted" in report
