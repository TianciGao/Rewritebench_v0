import json
from pathlib import Path

from sql_rewrite_bench.pocr.annotation_schema import ANNOTATION_SCHEMA_VERSION
from sql_rewrite_bench.pocr.draft_runner import build_diagnostic_drafts, diagnostic_draft_to_csv_rows
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory


REPO_ROOT = Path(__file__).resolve().parents[2]


def _candidate_root(tmp_path: Path, case_id: str) -> Path:
    candidate_root = tmp_path / "candidate_sql"
    candidate_root.mkdir()
    (candidate_root / f"{case_id}__postgres.sql").write_text("select 1;\n", encoding="utf-8")
    return candidate_root


def _annotation_payload(case_id: str = "PERF_0006") -> dict[str, object]:
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
                        "evidence_refs": [],
                        "confidence": "low",
                    }
                    for atom in contract.atoms
                ],
            }
    raise AssertionError(case_id)


def test_draft_runner_emits_annotation_missing_without_stage_a(tmp_path: Path) -> None:
    rows = build_diagnostic_drafts(
        REPO_ROOT,
        candidate_root=_candidate_root(tmp_path, "PERF_0006"),
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        case_ids=("PERF_0006",),
    )

    assert len(rows) == 1
    row = rows[0]
    assert row.skill_present is True
    assert row.candidate_present is True
    assert row.annotation_present is False
    assert row.stage_b_status == "annotation_missing"
    assert row.validated_operation_atoms_count == 0
    assert row.official_pocr_computed is False
    assert row.diagnostic_only is True


def test_draft_runner_keeps_stage_b_insufficient_without_independent_evidence(tmp_path: Path) -> None:
    candidate_root = _candidate_root(tmp_path, "PERF_0006")
    annotation_path = tmp_path / "annotations.jsonl"
    payload = _annotation_payload()
    payload["candidate_path"] = (candidate_root / "PERF_0006__postgres.sql").as_posix()
    annotation_path.write_text(json.dumps(payload) + "\n", encoding="utf-8")

    rows = build_diagnostic_drafts(
        REPO_ROOT,
        candidate_root=candidate_root,
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        case_ids=("PERF_0006",),
        annotation_jsonl=annotation_path,
    )

    assert rows[0].annotation_present is True
    assert rows[0].stage_b_status == "insufficient_evidence"
    assert rows[0].validated_operation_atoms_count == 0
    assert rows[0].expected_semantic_guard_atoms_count > 0

    csv_rows = diagnostic_draft_to_csv_rows(rows)
    assert csv_rows[0]["official_pocr_computed"] == "false"
    assert csv_rows[0]["diagnostic_only"] == "true"


def test_draft_runner_malformed_annotation_is_schema_invalid(tmp_path: Path) -> None:
    annotation_path = tmp_path / "annotations.jsonl"
    annotation_path.write_text('{"case_id": "PERF_0006", "atoms": [}\n', encoding="utf-8")

    rows = build_diagnostic_drafts(
        REPO_ROOT,
        candidate_root=_candidate_root(tmp_path, "PERF_0006"),
        method_id="noop_adapter",
        route_id="test_route",
        engine="postgres",
        case_ids=("PERF_0006",),
        annotation_jsonl=annotation_path,
    )

    assert rows[0].annotation_present is False
    assert rows[0].stage_b_status == "schema_invalid"
    assert rows[0].validated_operation_atoms_count == 0
