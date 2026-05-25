import csv
from pathlib import Path

import pytest

from sql_rewrite_bench.pocr.user_facade import run_pocr_diagnostic_user_facade


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_user_facade_emits_annotation_missing_rows_without_api(tmp_path: Path) -> None:
    candidate_root = tmp_path / "candidate_sql"
    candidate_root.mkdir()
    (candidate_root / "PERF_0006__postgres.sql").write_text("select 1;\n", encoding="utf-8")

    result = run_pocr_diagnostic_user_facade(
        repo_root=REPO_ROOT,
        run_id="pocr_facade_test",
        candidate_root=candidate_root,
        method_id="direct_llm_original",
        route_id="direct_llm_original_pg40_pocr_diagnostic",
        engine="postgres",
        live_enabled=False,
        case_ids=("PERF_0006",),
    )

    assert len(result.rows) == 1
    row = result.rows[0]
    assert row.annotation_status == "annotation_missing"
    assert row.stage_b_status == "annotation_missing"
    assert row.candidate_present is True
    assert row.skill_present is True
    assert row.expected_operation_atoms_count > 0
    assert row.semantic_guard_atoms_count > 0
    assert row.transformation_supported_operation_atoms_count == 0
    assert row.official_pocr_computed is False
    assert row.route_level_pocr_aggregated is False
    assert row.paper_metric_promoted is False
    assert result.output_paths is None


def test_user_facade_writes_temp_output_only_when_requested(tmp_path: Path) -> None:
    candidate_root = tmp_path / "candidate_sql"
    output_root = tmp_path / "user_output"
    candidate_root.mkdir()
    (candidate_root / "CONS_0005__postgres.sql").write_text("select 1;\n", encoding="utf-8")

    result = run_pocr_diagnostic_user_facade(
        repo_root=REPO_ROOT,
        run_id="pocr_facade_output_test",
        candidate_root=candidate_root,
        method_id="direct_llm_original",
        route_id="direct_llm_original_pg40_pocr_diagnostic",
        engine="postgres",
        live_enabled=False,
        output_root=output_root,
        case_ids=("CONS_0005",),
    )

    assert result.output_paths is not None
    assert result.output_paths.diagnostic_rows_csv.is_file()
    assert result.output_paths.diagnostic_rows_csv.resolve().is_relative_to(output_root.resolve())
    with result.output_paths.diagnostic_rows_csv.open(newline="", encoding="utf-8") as handle:
        row = next(csv.DictReader(handle))
    assert row["annotation_status"] == "annotation_missing"
    assert row["official_pocr_computed"] == "false"
    assert row["route_level_pocr_aggregated"] == "false"
    assert row["paper_metric_promoted"] == "false"


def test_user_facade_live_enabled_fails_closed_without_reading_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    candidate_root = tmp_path / "candidate_sql"
    candidate_root.mkdir()
    (candidate_root / "PERF_0006__postgres.sql").write_text("select 1;\n", encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "not-a-real-test-token")

    with pytest.raises(RuntimeError, match="live POCR annotation is not enabled"):
        run_pocr_diagnostic_user_facade(
            repo_root=REPO_ROOT,
            run_id="pocr_facade_live_disabled_test",
            candidate_root=candidate_root,
            method_id="direct_llm_original",
            route_id="direct_llm_original_pg40_pocr_diagnostic",
            engine="postgres",
            live_enabled=True,
            case_ids=("PERF_0006",),
        )
