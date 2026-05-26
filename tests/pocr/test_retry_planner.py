import csv
import json
from pathlib import Path

from sql_rewrite_bench.pocr.retry_planner import (
    plan_retries_from_checkpoint_state,
    plan_retries_from_manifest_csv,
    plan_retries_from_manifest_rows,
    retry_plan_rows_to_csv_rows,
)


def test_retry_planner_marks_malformed_timeout_and_provider_failure_eligible() -> None:
    rows = plan_retries_from_manifest_rows(
        [
            {
                "case_id": "PERF_0013",
                "pool": "PERF",
                "engine": "postgres",
                "method_id": "direct_llm_repair_1",
                "route_id": "direct_llm_repair_1_pg40_pocr_diagnostic",
                "candidate_sha256": "abc",
                "annotation_status": "malformed_json",
            },
            {"case_id": "PERF_0017", "annotation_status": "timeout"},
            {"case_id": "CONS_0005", "annotation_status": "schema_valid"},
            {"case_id": "PORT_0003", "annotation_status": "candidate_mismatch"},
        ]
    )

    by_case = {row.case_id: row for row in rows}
    assert by_case["PERF_0013"].retry_eligible is True
    assert by_case["PERF_0017"].retry_eligible is True
    assert by_case["PERF_0013"].retry_requires_explicit_flag is True
    assert by_case["CONS_0005"].retry_eligible is False
    assert by_case["PORT_0003"].recommendation == "fix_binding_before_retry"


def test_retry_planner_reads_manifest_csv(tmp_path: Path) -> None:
    path = tmp_path / "annotation_manifest.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["case_id", "annotation_status"], lineterminator="\n")
        writer.writeheader()
        writer.writerow({"case_id": "LONGTAIL_0012", "annotation_status": "provider_call_failed"})

    rows = plan_retries_from_manifest_csv(path)

    assert rows[0].case_id == "LONGTAIL_0012"
    assert rows[0].retry_eligible is True
    assert retry_plan_rows_to_csv_rows(rows)[0]["retry_eligible"] == "true"


def test_retry_planner_checkpoint_state_without_row_identity_returns_empty(tmp_path: Path) -> None:
    path = tmp_path / "checkpoint_state.json"
    path.write_text(json.dumps({"rows": 40, "status_counts": {"timeout": 2}}), encoding="utf-8")

    assert plan_retries_from_checkpoint_state(path) == []


def test_retry_planner_checkpoint_state_row_statuses_are_supported(tmp_path: Path) -> None:
    path = tmp_path / "checkpoint_state.json"
    path.write_text(json.dumps({"row_statuses": {"PERF_0052": "timeout"}}), encoding="utf-8")

    rows = plan_retries_from_checkpoint_state(path)

    assert rows[0].case_id == "PERF_0052"
    assert rows[0].current_status == "timeout"
    assert rows[0].retry_eligible is True
