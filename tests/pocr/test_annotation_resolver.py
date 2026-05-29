import json
from pathlib import Path

from sql_rewrite_bench.pocr.annotation_resolver import (
    annotation_artifacts_to_csv_rows,
    resolve_annotation_artifacts,
)
from sql_rewrite_bench.pocr.annotation_schema import ANNOTATION_SCHEMA_VERSION
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory


REPO_ROOT = Path(__file__).resolve().parents[2]


def _annotation_payload(case_id: str = "PERF_0006", *, route_id: str = "test_route") -> dict[str, object]:
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
                "route_id": route_id,
                "candidate_path": f"candidate_sql/{case_id}__postgres.sql",
                "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
                "atoms": [
                    {
                        "atom_id": atom.atom_id,
                        "atom_type": atom.category,
                        "expected": True,
                        "observed_status": "implemented",
                        "rationale_short": "Fixture annotation, not independent evidence.",
                        "evidence_refs": [],
                        "confidence": "low",
                    }
                    for atom in contract.atoms
                ],
            }
    raise AssertionError(case_id)


def test_annotation_resolver_reads_valid_annotation_jsonl(tmp_path: Path) -> None:
    annotation_path = tmp_path / "annotations.jsonl"
    annotation_path.write_text(json.dumps(_annotation_payload()) + "\n", encoding="utf-8")

    rows = resolve_annotation_artifacts(
        REPO_ROOT,
        annotation_jsonl=annotation_path,
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        case_ids=("PERF_0006",),
    )

    assert rows[0].annotation_status == "present"
    assert rows[0].annotation is not None
    assert rows[0].candidate_ref.endswith("PERF_0006__postgres.sql")
    assert annotation_artifacts_to_csv_rows(rows)[0]["annotation_status"] == "present"


def test_annotation_resolver_reports_missing_annotation_artifact(tmp_path: Path) -> None:
    rows = resolve_annotation_artifacts(
        REPO_ROOT,
        annotation_jsonl=tmp_path / "missing.jsonl",
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        case_ids=("CONS_0005",),
    )

    assert rows[0].annotation_status == "missing"
    assert rows[0].annotation is None


def test_annotation_resolver_reports_malformed_json(tmp_path: Path) -> None:
    annotation_path = tmp_path / "annotations.jsonl"
    annotation_path.write_text('{"case_id": "PERF_0006", "atoms": [}\n', encoding="utf-8")

    rows = resolve_annotation_artifacts(
        REPO_ROOT,
        annotation_jsonl=annotation_path,
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        case_ids=("PERF_0006",),
    )

    assert rows[0].annotation_status == "malformed_json"
    assert "malformed_json" in rows[0].issue_codes
    assert rows[0].annotation is None


def test_annotation_resolver_reports_schema_invalid_annotation(tmp_path: Path) -> None:
    payload = _annotation_payload()
    payload["atoms"] = payload["atoms"][:-1]
    annotation_path = tmp_path / "annotations.jsonl"
    annotation_path.write_text(json.dumps(payload) + "\n", encoding="utf-8")

    rows = resolve_annotation_artifacts(
        REPO_ROOT,
        annotation_jsonl=annotation_path,
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        case_ids=("PERF_0006",),
    )

    assert rows[0].annotation_status == "schema_invalid"
    assert "missing_atom_judgment" in rows[0].issue_codes


def test_annotation_resolver_reports_route_mismatch(tmp_path: Path) -> None:
    annotation_path = tmp_path / "annotations.jsonl"
    annotation_path.write_text(json.dumps(_annotation_payload(route_id="other_route")) + "\n", encoding="utf-8")

    rows = resolve_annotation_artifacts(
        REPO_ROOT,
        annotation_jsonl=annotation_path,
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        case_ids=("PERF_0006",),
    )

    assert rows[0].annotation_status == "route_mismatch"
    assert "annotation_route_id_mismatch" in rows[0].issue_codes


def test_annotation_resolver_reports_case_mismatch(tmp_path: Path) -> None:
    annotation_path = tmp_path / "annotations.jsonl"
    annotation_path.write_text(
        json.dumps({"case_id": "CONS_0005", "annotation": _annotation_payload("PERF_0006")}) + "\n",
        encoding="utf-8",
    )

    rows = resolve_annotation_artifacts(
        REPO_ROOT,
        annotation_jsonl=annotation_path,
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        case_ids=("PERF_0006",),
    )

    assert rows[0].annotation_status == "case_mismatch"
    assert "annotation_case_id_mismatch" in rows[0].issue_codes
