import csv
import json
from pathlib import Path

import pytest

from sql_rewrite_bench.pocr.annotation_schema import ANNOTATION_SCHEMA_VERSION
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory
from sql_rewrite_bench.pocr.user_facade import run_pocr_diagnostic_user_facade


REPO_ROOT = Path(__file__).resolve().parents[2]


def _annotation_payload(
    case_id: str = "PERF_0006",
    *,
    method_id: str = "direct_llm_original",
    route_id: str = "direct_llm_original_pg40_pocr_diagnostic",
) -> dict[str, object]:
    inventory = build_common_core_inventory(REPO_ROOT)
    for member, result in zip(inventory.members, inventory.parse_results, strict=True):
        if member.case_id != case_id:
            continue
        contract = result.contract
        assert contract is not None
        first_operation = True
        atoms: list[dict[str, object]] = []
        for atom in contract.atoms:
            implemented = atom.category == "operation_atom" and first_operation
            if implemented:
                first_operation = False
            atoms.append(
                {
                    "atom_id": atom.atom_id,
                    "atom_type": atom.category,
                    "expected": True,
                    "observed_status": "implemented" if implemented else "not_implemented",
                    "rationale_short": "Fixture replay annotation, not official POCR evidence.",
                    "evidence_refs": (
                        ["candidate_sql_span:rewritten_marker", "source_candidate_diff:changed"]
                        if implemented
                        else []
                    ),
                    "confidence": "low",
                }
            )
        return {
            "case_id": case_id,
            "pool": member.pool,
            "engine": "postgres",
            "method_id": method_id,
            "route_id": route_id,
            "candidate_path": f"candidate_sql/{case_id}__postgres.sql",
            "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
            "atoms": atoms,
        }
    raise AssertionError(case_id)


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


def test_user_facade_replays_valid_annotation_jsonl(tmp_path: Path) -> None:
    candidate_root = tmp_path / "candidate_sql"
    candidate_root.mkdir()
    (candidate_root / "PERF_0006__postgres.sql").write_text("select 1 as rewritten_marker;\n", encoding="utf-8")
    annotation_path = tmp_path / "annotations.jsonl"
    annotation_path.write_text(json.dumps(_annotation_payload()) + "\n", encoding="utf-8")

    result = run_pocr_diagnostic_user_facade(
        repo_root=REPO_ROOT,
        run_id="pocr_facade_replay_test",
        candidate_root=candidate_root,
        method_id="direct_llm_original",
        route_id="direct_llm_original_pg40_pocr_diagnostic",
        engine="postgres",
        annotation_jsonl=annotation_path,
        live_enabled=False,
        case_ids=("PERF_0006",),
    )

    row = result.rows[0]
    assert row.annotation_status == "schema_valid"
    assert row.transformation_supported_operation_atoms_count == 1
    assert row.official_pocr_computed is False
    assert row.route_level_pocr_aggregated is False
    assert row.paper_metric_promoted is False


def test_user_facade_missing_annotation_jsonl_row_remains_annotation_missing(tmp_path: Path) -> None:
    candidate_root = tmp_path / "candidate_sql"
    candidate_root.mkdir()
    (candidate_root / "PERF_0006__postgres.sql").write_text("select 1;\n", encoding="utf-8")
    annotation_path = tmp_path / "annotations.jsonl"
    annotation_path.write_text(json.dumps(_annotation_payload("CONS_0005")) + "\n", encoding="utf-8")

    result = run_pocr_diagnostic_user_facade(
        repo_root=REPO_ROOT,
        run_id="pocr_facade_missing_replay_test",
        candidate_root=candidate_root,
        method_id="direct_llm_original",
        route_id="direct_llm_original_pg40_pocr_diagnostic",
        engine="postgres",
        annotation_jsonl=annotation_path,
        live_enabled=False,
        case_ids=("PERF_0006",),
    )

    assert result.rows[0].annotation_status == "annotation_missing"
    assert result.rows[0].stage_b_status == "annotation_missing"


def test_user_facade_malformed_jsonl_row_fails_closed(tmp_path: Path) -> None:
    candidate_root = tmp_path / "candidate_sql"
    candidate_root.mkdir()
    (candidate_root / "PERF_0006__postgres.sql").write_text("select 1;\n", encoding="utf-8")
    annotation_path = tmp_path / "annotations.jsonl"
    annotation_path.write_text('{"case_id": "PERF_0006", "atoms": [}\n', encoding="utf-8")

    result = run_pocr_diagnostic_user_facade(
        repo_root=REPO_ROOT,
        run_id="pocr_facade_malformed_replay_test",
        candidate_root=candidate_root,
        method_id="direct_llm_original",
        route_id="direct_llm_original_pg40_pocr_diagnostic",
        engine="postgres",
        annotation_jsonl=annotation_path,
        live_enabled=False,
        case_ids=("PERF_0006",),
    )

    row = result.rows[0]
    assert row.annotation_status == "schema_invalid"
    assert row.stage_b_status == "schema_invalid"
    assert row.schema_invalid_atoms_count == row.expected_operation_atoms_count
    assert "malformed_json" in row.boundary_notes


def test_user_facade_route_mismatch_fails_closed(tmp_path: Path) -> None:
    candidate_root = tmp_path / "candidate_sql"
    candidate_root.mkdir()
    (candidate_root / "PERF_0006__postgres.sql").write_text("select 1 as rewritten_marker;\n", encoding="utf-8")
    annotation_path = tmp_path / "annotations.jsonl"
    annotation_path.write_text(
        json.dumps(_annotation_payload(route_id="direct_llm_original_other_route")) + "\n",
        encoding="utf-8",
    )

    result = run_pocr_diagnostic_user_facade(
        repo_root=REPO_ROOT,
        run_id="pocr_facade_route_mismatch_replay_test",
        candidate_root=candidate_root,
        method_id="direct_llm_original",
        route_id="direct_llm_original_pg40_pocr_diagnostic",
        engine="postgres",
        annotation_jsonl=annotation_path,
        live_enabled=False,
        case_ids=("PERF_0006",),
    )

    row = result.rows[0]
    assert row.annotation_status == "schema_invalid"
    assert row.transformation_supported_operation_atoms_count == 0
    assert "route_mismatch" in row.boundary_notes


def test_user_facade_duplicate_annotation_rows_fail_closed(tmp_path: Path) -> None:
    candidate_root = tmp_path / "candidate_sql"
    candidate_root.mkdir()
    (candidate_root / "PERF_0006__postgres.sql").write_text("select 1 as rewritten_marker;\n", encoding="utf-8")
    annotation_path = tmp_path / "annotations.jsonl"
    payload = json.dumps(_annotation_payload())
    annotation_path.write_text(payload + "\n" + payload + "\n", encoding="utf-8")

    result = run_pocr_diagnostic_user_facade(
        repo_root=REPO_ROOT,
        run_id="pocr_facade_duplicate_replay_test",
        candidate_root=candidate_root,
        method_id="direct_llm_original",
        route_id="direct_llm_original_pg40_pocr_diagnostic",
        engine="postgres",
        annotation_jsonl=annotation_path,
        live_enabled=False,
        case_ids=("PERF_0006",),
    )

    row = result.rows[0]
    assert row.annotation_status == "schema_invalid"
    assert "duplicate_annotation_rows" in row.boundary_notes
