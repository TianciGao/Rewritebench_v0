import csv
from pathlib import Path

from sql_rewrite_bench.pocr.diagnostic_output_schema import POCRDiagnosticRow, summarize_by_pool
from sql_rewrite_bench.pocr.user_output_adapter import write_pocr_diagnostic_user_outputs


def _row() -> POCRDiagnosticRow:
    return POCRDiagnosticRow(
        run_id="pocr_output_test",
        case_id="PERF_0006",
        pool="PERF",
        engine="postgres",
        method_id="direct_llm_original",
        route_id="direct_llm_original_pg40_pocr_diagnostic",
        candidate_path="runs/user/example/candidate_sql/PERF_0006__postgres.sql",
        candidate_present=True,
        skill_present=True,
        annotation_status="annotation_missing",
        stage_b_status="annotation_missing",
        expected_operation_atoms_count=2,
        stage_a_implemented_operation_atoms_count=0,
        transformation_supported_operation_atoms_count=0,
        presence_only_operation_atoms_count=0,
        insufficient_transformation_evidence_operation_atoms_count=0,
        rejected_noop_equivalent_operation_atoms_count=0,
        schema_invalid_atoms_count=0,
        semantic_guard_atoms_count=2,
    )


def test_user_output_adapter_writes_only_under_supplied_output_root(tmp_path: Path) -> None:
    rows = (_row(),)
    summaries = summarize_by_pool(rows)

    paths = write_pocr_diagnostic_user_outputs(
        output_root=tmp_path,
        run_id="pocr_output_test",
        rows=rows,
        summaries=summaries,
    )

    expected_prefix = tmp_path.resolve()
    for path in (
        paths.diagnostic_rows_csv,
        paths.diagnostic_summary_by_pool_csv,
        paths.diagnostic_log,
        paths.diagnostic_report_md,
    ):
        assert path.is_file()
        assert path.resolve().is_relative_to(expected_prefix)

    assert paths.diagnostic_rows_csv.as_posix().endswith(
        "results/pocr_output_test/pocr/diagnostic_rows.csv"
    )
    assert paths.diagnostic_summary_by_pool_csv.as_posix().endswith(
        "results/pocr_output_test/pocr/diagnostic_summary_by_pool.csv"
    )
    assert paths.diagnostic_log.as_posix().endswith("logs/pocr_output_test/pocr/pocr_diagnostic.log")
    assert paths.diagnostic_report_md.as_posix().endswith("reports/pocr_output_test/pocr_diagnostic.md")

    with paths.diagnostic_rows_csv.open(newline="", encoding="utf-8") as handle:
        row = next(csv.DictReader(handle))
    assert row["official_pocr_computed"] == "false"
    assert row["route_level_pocr_aggregated"] == "false"
    assert row["paper_metric_promoted"] == "false"

    report = paths.diagnostic_report_md.read_text(encoding="utf-8")
    assert "This is not official POCR." in report
    assert "No route-level POCR score is emitted." in report
    assert "Semantic guard atoms are not part of operation coverage numerator." in report
    assert "No paper-facing metric is promoted." in report
