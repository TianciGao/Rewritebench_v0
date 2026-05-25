from pathlib import Path

from sql_rewrite_bench.pocr.annotation_schema import ANNOTATION_SCHEMA_VERSION, annotation_from_mapping
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory
from sql_rewrite_bench.pocr.operation_evidence_policy import validate_transformation_stage_b
from sql_rewrite_bench.pocr.real_route_diagnostic_runner import (
    METHOD_ID,
    ROUTE_ID,
    diagnostic_row_from_stage_b,
    discover_direct_llm_original_candidate_roots,
    load_real_route_candidates,
    schema_invalid_diagnostic_row,
    selected_candidate_root,
    summary_rows,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def _case_ids() -> tuple[str, ...]:
    inventory = build_common_core_inventory(REPO_ROOT)
    return tuple(member.case_id for member in inventory.members)


def _write_pg40_root(root: Path) -> None:
    root.mkdir(parents=True)
    for case_id in _case_ids():
        (root / f"{case_id}__postgres.sql").write_text("select 1;\n", encoding="utf-8")


def test_direct_llm_root_discovery_selects_one_unambiguous_pg40_root(tmp_path: Path) -> None:
    selected = tmp_path / "runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql"
    repair = tmp_path / "runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql"
    _write_pg40_root(selected)
    _write_pg40_root(repair)

    rows = discover_direct_llm_original_candidate_roots(REPO_ROOT, runs_root=tmp_path / "runs/user")

    assert selected_candidate_root(rows).as_posix().endswith("direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql")
    selected_rows = [row for row in rows if row.selected]
    assert len(selected_rows) == 1
    assert selected_rows[0].inferred_method_id == METHOD_ID
    assert selected_rows[0].common_core_match_count == 40
    assert all(not row.selected for row in rows if row.inferred_method_id != METHOD_ID)


def test_direct_llm_root_discovery_fails_closed_for_ambiguous_roots(tmp_path: Path) -> None:
    first = tmp_path / "runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql"
    second = tmp_path / "runs/user/direct_llm_original_pg40_duplicate_v0__postgres/candidate_sql"
    _write_pg40_root(first)
    _write_pg40_root(second)

    rows = discover_direct_llm_original_candidate_roots(REPO_ROOT, runs_root=tmp_path / "runs/user")

    assert selected_candidate_root(rows) is None
    assert sum(row.common_core_match_count == 40 for row in rows) == 2
    assert all(not row.selected for row in rows)


def test_no_candidate_root_means_no_selected_root_or_api_path(tmp_path: Path) -> None:
    rows = discover_direct_llm_original_candidate_roots(REPO_ROOT, runs_root=tmp_path / "runs/user")

    assert rows == ()
    assert selected_candidate_root(rows) is None


def test_selected_root_must_resolve_common_core_case_ids(tmp_path: Path) -> None:
    root = tmp_path / "runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql"
    _write_pg40_root(root)

    sources = load_real_route_candidates(REPO_ROOT, candidate_root=root)

    assert len(sources) == 40
    assert all(source.resolver_status == "resolved" for source in sources)
    assert {source.case_id for source in sources} == set(_case_ids())
    assert all(source.method_id == METHOD_ID for source in sources)
    assert all(source.route_id == ROUTE_ID for source in sources)


def test_diagnostic_rows_never_compute_official_pocr_or_route_aggregation() -> None:
    sources = load_real_route_candidates(
        REPO_ROOT,
        candidate_root=Path("runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql"),
        method_id=METHOD_ID,
        route_id=ROUTE_ID,
    )
    source = next(row for row in sources if row.case_id == "PERF_0006")
    inventory = build_common_core_inventory(REPO_ROOT)
    contract = next(result.contract for member, result in zip(inventory.members, inventory.parse_results, strict=True) if member.case_id == "PERF_0006")
    assert contract is not None
    annotation = annotation_from_mapping(
        {
            "case_id": "PERF_0006",
            "pool": "PERF",
            "engine": "postgres",
            "method_id": METHOD_ID,
            "route_id": ROUTE_ID,
            "candidate_id": "candidate_001",
            "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
            "atoms": [
                {
                    "atom_id": atom.atom_id,
                    "atom_type": atom.category,
                    "expected": True,
                    "observed_status": "implemented" if atom.category == "operation_atom" else "unclear",
                    "rationale_short": "fixture rationale",
                    "evidence_refs": ["candidate_sql_span:WITH", "source_candidate_diff:changed"]
                    if atom.category == "operation_atom"
                    else [],
                    "confidence": "medium",
                }
                for atom in contract.atoms
            ],
        }
    )
    stage_b = validate_transformation_stage_b(
        contract,
        annotation,
        source_sql="select * from lineitem;",
        candidate_sql="WITH staged AS (select * from lineitem) select * from staged;",
        positive_sql="WITH staged AS (select * from lineitem) select * from staged;",
    )

    row = diagnostic_row_from_stage_b(source, contract, annotation, stage_b, annotation_status="schema_valid")

    assert row.diagnostic_only is True
    assert row.official_pocr_computed is False
    assert row.route_level_pocr_aggregated is False
    assert row.semantic_guard_atoms_count == len(contract.semantic_guard_atoms)
    assert row.transformation_supported_operation_atoms_count >= 1


def test_schema_invalid_diagnostic_row_is_fail_closed() -> None:
    sources = load_real_route_candidates(
        REPO_ROOT,
        candidate_root=Path("runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql"),
        method_id=METHOD_ID,
        route_id=ROUTE_ID,
    )
    source = sources[0]
    inventory = build_common_core_inventory(REPO_ROOT)
    contract = next(result.contract for member, result in zip(inventory.members, inventory.parse_results, strict=True) if member.case_id == source.case_id)
    assert contract is not None

    row = schema_invalid_diagnostic_row(source, contract, reason="malformed JSON")

    assert row.annotation_status == "schema_invalid"
    assert row.stage_b_status == "schema_invalid"
    assert row.transformation_supported_operation_atoms_count == 0
    assert row.official_pocr_computed is False


def test_summary_rows_are_pool_diagnostics_not_route_level_pocr() -> None:
    row = schema_invalid_diagnostic_row(
        load_real_route_candidates(
            REPO_ROOT,
            candidate_root=Path("runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql"),
            method_id=METHOD_ID,
            route_id=ROUTE_ID,
        )[0],
        next(result.contract for result in build_common_core_inventory(REPO_ROOT).parse_results if result.contract is not None),
        reason="fixture",
    )

    summary = summary_rows([row])

    assert {item["pool"] for item in summary} == {"PERF", "CONS", "PORT", "LONGTAIL"}
    assert all(item["diagnostic_only"] == "true" for item in summary)
    assert all(item["official_pocr_computed"] == "false" for item in summary)
