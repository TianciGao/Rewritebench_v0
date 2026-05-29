from pathlib import Path

from sql_rewrite_bench.pocr.annotation_schema import ANNOTATION_SCHEMA_VERSION, annotation_from_mapping
from sql_rewrite_bench.pocr.calibration_runner import (
    CalibrationResultRow,
    FULL40_POSITIVE_ROUTE_ID,
    apply_calibration_risks,
    calibration_result_from_stage_b,
    load_calibration_candidates,
    schema_invalid_calibration_result,
)
from sql_rewrite_bench.pocr.inventory import build_common_core_inventory
from sql_rewrite_bench.pocr.operation_evidence_policy import validate_transformation_stage_b


REPO_ROOT = Path(__file__).resolve().parents[2]


def _contract(case_id: str = "CONS_0005"):
    inventory = build_common_core_inventory(REPO_ROOT)
    for member, result in zip(inventory.members, inventory.parse_results, strict=True):
        if member.case_id == case_id:
            assert result.contract is not None
            return result.contract
    raise AssertionError(case_id)


def _annotation_payload(contract, *, op_refs: list[str] | None = None, guard_refs: list[str] | None = None):
    return {
        "case_id": contract.case_id,
        "pool": contract.pool,
        "engine": "postgres",
        "method_id": "fixture_method",
        "route_id": "fixture_route",
        "candidate_id": "candidate_001",
        "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
        "atoms": [
            {
                "atom_id": atom.atom_id,
                "atom_type": atom.category,
                "expected": True,
                "observed_status": "implemented",
                "rationale_short": "Fixture annotation, not independent evidence.",
                "evidence_refs": (op_refs or []) if atom.category == "operation_atom" else (guard_refs or []),
                "confidence": "medium",
            }
            for atom in contract.atoms
        ],
    }


def test_calibration_candidate_loader_maps_positive_and_noop_controls() -> None:
    candidates = load_calibration_candidates(
        REPO_ROOT,
        case_ids=("PERF_0006",),
        noop_candidate_root=Path("runs/user/common_core_pg_noop_db_checker/candidate_sql"),
    )

    assert {candidate.candidate_class for candidate in candidates} == {"positive_control", "noop_control"}
    positive = next(candidate for candidate in candidates if candidate.candidate_class == "positive_control")
    noop = next(candidate for candidate in candidates if candidate.candidate_class == "noop_control")
    assert positive.method_id == "human_positive_control"
    assert positive.route_id == "pocr_positive_control_calibration"
    assert positive.candidate_sql_path.as_posix() == "cases/PERF/PERF_0006/sql/pos_01.sql"
    assert noop.method_id == "sqlglot_noop"
    assert noop.candidate_sql_path.as_posix().endswith("PERF_0006__postgres.sql")
    assert positive.candidate_source_status == "ready"
    assert noop.candidate_source_status == "ready"


def test_calibration_candidate_loader_maps_all_40_cases() -> None:
    inventory = build_common_core_inventory(REPO_ROOT)
    case_ids = tuple(member.case_id for member in inventory.members)

    candidates = load_calibration_candidates(
        REPO_ROOT,
        case_ids=case_ids,
        noop_candidate_root=Path("runs/user/common_core_pg_noop_db_checker/candidate_sql"),
        positive_route_id=FULL40_POSITIVE_ROUTE_ID,
    )

    assert len(case_ids) == 40
    assert len(candidates) == 80
    assert {candidate.case_id for candidate in candidates} == set(case_ids)
    assert all(candidate.candidate_source_status == "ready" for candidate in candidates)
    positives = [candidate for candidate in candidates if candidate.candidate_class == "positive_control"]
    noops = [candidate for candidate in candidates if candidate.candidate_class == "noop_control"]
    assert len(positives) == 40
    assert len(noops) == 40
    assert {candidate.route_id for candidate in positives} == {FULL40_POSITIVE_ROUTE_ID}
    assert all(candidate.candidate_sql_path.as_posix().endswith("sql/pos_01.sql") for candidate in positives)
    assert all("common_core_pg_noop_db_checker" in candidate.candidate_sql_path.as_posix() for candidate in noops)


def test_calibration_rows_are_diagnostic_only_and_semantic_guards_not_operation_numerator() -> None:
    candidates = load_calibration_candidates(REPO_ROOT, case_ids=("CONS_0005",))
    candidate = next(row for row in candidates if row.candidate_class == "positive_control")
    contract = _contract("CONS_0005")
    candidate_sql = (REPO_ROOT / candidate.candidate_sql_path).read_text(encoding="utf-8-sig")
    source_sql = (REPO_ROOT / candidate.source_sql_path).read_text(encoding="utf-8-sig")
    positive_sql = (REPO_ROOT / candidate.positive_sql_path).read_text(encoding="utf-8-sig")
    first_line = candidate_sql.strip().splitlines()[0]
    payload = _annotation_payload(contract, op_refs=[], guard_refs=[f"candidate_sql_span:{first_line}"])
    payload["method_id"] = candidate.method_id
    payload["route_id"] = candidate.route_id
    payload["candidate_path"] = candidate.candidate_sql_path.as_posix()
    payload.pop("candidate_id")
    annotation = annotation_from_mapping(payload)
    stage_b = validate_transformation_stage_b(contract, annotation, source_sql=source_sql, candidate_sql=candidate_sql, positive_sql=positive_sql)

    row = calibration_result_from_stage_b(candidate, contract, annotation, stage_b)

    assert row.diagnostic_only is True
    assert row.official_pocr_computed is False
    assert row.route_level_pocr_aggregated is False
    assert row.transformation_supported_operation_atoms_count == 0
    assert row.semantic_guard_atoms_count == len(contract.semantic_guard_atoms)


def test_noop_over_acceptance_is_flagged_as_noop_transformation_overaccept_risk() -> None:
    rows = (
        _row("CASE_A", "positive_control", validated=3),
        _row("CASE_A", "noop_control", validated=2),
    )

    marked = apply_calibration_risks(rows)

    assert {row.calibration_risk for row in marked} == {"noop_transformation_overaccept_risk"}


def test_positive_clearly_above_noop_is_low_risk() -> None:
    rows = (
        _row("CASE_A", "positive_control", validated=3),
        _row("CASE_A", "noop_control", validated=0),
    )

    marked = apply_calibration_risks(rows)

    assert {row.calibration_risk for row in marked} == {"low"}


def test_positive_control_no_support_is_reported_as_gap() -> None:
    rows = (
        _row("CASE_A", "positive_control", validated=0),
        _row("CASE_A", "noop_control", validated=0),
    )

    marked = apply_calibration_risks(rows)

    assert {row.calibration_risk for row in marked} == {"atom_or_positive_alignment_gap"}


def test_schema_invalid_calibration_result_is_fail_closed() -> None:
    candidate = load_calibration_candidates(REPO_ROOT, case_ids=("CONS_0005",))[0]
    contract = _contract("CONS_0005")

    row = schema_invalid_calibration_result(candidate, contract, reason="malformed JSON")

    assert row.transformation_supported_operation_atoms_count == 0
    assert row.schema_invalid_atoms_count == len(contract.operation_atoms)
    assert row.official_pocr_computed is False
    assert row.route_level_pocr_aggregated is False
    assert row.calibration_risk == "schema_invalid"


def test_unsupported_evidence_ref_is_rejected_in_calibration_fixture() -> None:
    candidate = load_calibration_candidates(REPO_ROOT, case_ids=("CONS_0005",))[0]
    contract = _contract("CONS_0005")
    candidate_sql = (REPO_ROOT / candidate.candidate_sql_path).read_text(encoding="utf-8-sig")
    source_sql = (REPO_ROOT / candidate.source_sql_path).read_text(encoding="utf-8-sig")
    positive_sql = (REPO_ROOT / candidate.positive_sql_path).read_text(encoding="utf-8-sig")
    payload = _annotation_payload(contract, op_refs=["candidate_sql: SELECT 1"])
    payload["method_id"] = candidate.method_id
    payload["route_id"] = candidate.route_id
    payload["candidate_path"] = candidate.candidate_sql_path.as_posix()
    payload.pop("candidate_id")

    stage_b = validate_transformation_stage_b(
        contract,
        annotation_from_mapping(payload),
        source_sql=source_sql,
        candidate_sql=candidate_sql,
        positive_sql=positive_sql,
    )

    assert {
        atom.evidence_status for atom in stage_b.atom_results if atom.atom_type == "operation_atom"
    } == {"invalid_ref"}
    assert stage_b.transformation_supported_operation_atoms_count == 0


def _row(case_id: str, candidate_class: str, *, validated: int) -> CalibrationResultRow:
    return CalibrationResultRow(
        case_id=case_id,
        pool="CONS",
        candidate_class=candidate_class,
        method_id="fixture",
        route_id="fixture",
        expected_operation_atoms_count=3,
        stage_a_implemented_operation_atoms_count=validated,
        presence_only_operation_atoms_count=0,
        transformation_supported_operation_atoms_count=validated,
        insufficient_transformation_evidence_operation_atoms_count=0,
        rejected_noop_equivalent_operation_atoms_count=0,
        schema_invalid_atoms_count=0,
        semantic_guard_atoms_count=1,
        diagnostic_only=True,
        official_pocr_computed=False,
        route_level_pocr_aggregated=False,
        calibration_risk="pending_pair_comparison",
    )
