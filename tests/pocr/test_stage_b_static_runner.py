import json
from pathlib import Path

from sql_rewrite_bench.pocr.annotation_schema import ANNOTATION_SCHEMA_VERSION
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory
from sql_rewrite_bench.pocr.stage_b_static_runner import (
    build_static_stage_b_diagnostic_rows,
    static_stage_b_diagnostic_to_csv_rows,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def _candidate_root(tmp_path: Path, case_id: str, sql: str = "select 1;\n") -> Path:
    candidate_root = tmp_path / "candidate_sql"
    candidate_root.mkdir()
    (candidate_root / f"{case_id}__postgres.sql").write_text(sql, encoding="utf-8")
    return candidate_root


def _annotation_payload(case_id: str = "PERF_0006", *, op_refs: list[str] | None = None) -> dict[str, object]:
    inventory = build_common_core_inventory(REPO_ROOT)
    for member, result in zip(inventory.members, inventory.parse_results, strict=True):
        if member.case_id == case_id:
            contract = result.contract
            assert contract is not None
            return {
                "case_id": case_id,
                "pool": member.pool,
                "engine": "postgres",
                "method_id": "noop_adapter",
                "route_id": "test_route",
                "candidate_path": f"candidate_sql/{case_id}__postgres.sql",
                "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
                "atoms": [
                    {
                        "atom_id": atom.atom_id,
                        "atom_type": atom.category,
                        "expected": True,
                        "observed_status": "implemented",
                        "rationale_short": "Fixture annotation, not independent evidence.",
                        "evidence_refs": (op_refs or []) if index == 0 and atom.category == "operation_atom" else [],
                        "confidence": "low",
                    }
                    for index, atom in enumerate(contract.atoms)
                ],
            }
    raise AssertionError(case_id)


def test_static_runner_validates_only_explicit_static_refs(tmp_path: Path) -> None:
    candidate_root = _candidate_root(tmp_path, "PERF_0006", "select 1;\n")
    annotation_path = tmp_path / "annotations.jsonl"
    payload = _annotation_payload(op_refs=["candidate_sql_span:select 1"])
    payload["candidate_path"] = (candidate_root / "PERF_0006__postgres.sql").as_posix()
    annotation_path.write_text(json.dumps(payload) + "\n", encoding="utf-8")

    rows = build_static_stage_b_diagnostic_rows(
        REPO_ROOT,
        candidate_root=candidate_root,
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        annotation_jsonl=annotation_path,
        case_ids=("PERF_0006",),
    )

    assert rows[0].annotation_present is True
    assert rows[0].annotation_status == "present"
    assert rows[0].stage_b_status == "static_evidence_partial"
    assert rows[0].static_validated_operation_atoms_count == 1
    assert rows[0].official_pocr_computed is False
    assert rows[0].diagnostic_only is True

    csv_rows = static_stage_b_diagnostic_to_csv_rows(rows)
    assert csv_rows[0]["official_pocr_computed"] == "false"
    assert csv_rows[0]["diagnostic_only"] == "true"


def test_static_runner_remains_insufficient_without_evidence_refs(tmp_path: Path) -> None:
    candidate_root = _candidate_root(tmp_path, "PERF_0006", "select 1;\n")
    annotation_path = tmp_path / "annotations.jsonl"
    payload = _annotation_payload()
    payload["candidate_path"] = (candidate_root / "PERF_0006__postgres.sql").as_posix()
    annotation_path.write_text(json.dumps(payload) + "\n", encoding="utf-8")

    rows = build_static_stage_b_diagnostic_rows(
        REPO_ROOT,
        candidate_root=candidate_root,
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        annotation_jsonl=annotation_path,
        case_ids=("PERF_0006",),
    )

    assert rows[0].stage_b_status == "insufficient_evidence"
    assert rows[0].static_validated_operation_atoms_count == 0


def test_static_runner_malformed_annotation_is_schema_invalid(tmp_path: Path) -> None:
    annotation_path = tmp_path / "annotations.jsonl"
    annotation_path.write_text('{"case_id": "PERF_0006", "atoms": [}\n', encoding="utf-8")

    rows = build_static_stage_b_diagnostic_rows(
        REPO_ROOT,
        candidate_root=_candidate_root(tmp_path, "PERF_0006"),
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        annotation_jsonl=annotation_path,
        case_ids=("PERF_0006",),
    )

    assert rows[0].annotation_status == "malformed_json"
    assert rows[0].annotation_present is False
    assert rows[0].stage_b_status == "schema_invalid"
    assert rows[0].static_validated_operation_atoms_count == 0


def test_static_runner_missing_annotation_is_annotation_missing(tmp_path: Path) -> None:
    rows = build_static_stage_b_diagnostic_rows(
        REPO_ROOT,
        candidate_root=_candidate_root(tmp_path, "PERF_0006"),
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        case_ids=("PERF_0006",),
    )

    assert rows[0].annotation_status == "missing"
    assert rows[0].stage_b_status == "annotation_missing"
    assert rows[0].static_validated_operation_atoms_count == 0
