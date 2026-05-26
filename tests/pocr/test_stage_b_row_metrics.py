import csv
import hashlib
from pathlib import Path

from sql_rewrite_bench.pocr.diagnostic_output_schema import POCRDiagnosticRow
from sql_rewrite_bench.pocr.stage_b_row_metrics import (
    export_stage_b_row_metrics,
    stage_b_row_metric_fields,
)


def _candidate(tmp_path: Path, case_id: str) -> Path:
    path = tmp_path / f"{case_id}__postgres.sql"
    path.write_text(f"select '{case_id}' as marker;\n", encoding="utf-8")
    return path


def _row(
    *,
    tmp_path: Path,
    case_id: str = "PERF_0006",
    annotation_status: str = "schema_valid",
    stage_b_status: str = "transformation_evidence_partial",
    expected: int = 4,
    supported: int = 1,
    presence_only: int = 0,
    insufficient: int = 0,
    rejected_noop: int = 0,
    semantic_guards: int = 2,
    candidate_present: bool = True,
    boundary_notes: str = "Stage B transformation-aware validation is diagnostic only.",
) -> POCRDiagnosticRow:
    candidate_path = _candidate(tmp_path, case_id) if candidate_present else tmp_path / f"{case_id}__postgres.sql"
    return POCRDiagnosticRow(
        run_id="pocr_stage_b_metrics_test",
        case_id=case_id,
        pool=case_id.split("_", maxsplit=1)[0],
        engine="postgres",
        method_id="method",
        route_id="route",
        candidate_path=candidate_path.as_posix(),
        candidate_present=candidate_present,
        skill_present=True,
        annotation_status=annotation_status,
        stage_b_status=stage_b_status,
        expected_operation_atoms_count=expected,
        stage_a_implemented_operation_atoms_count=supported,
        transformation_supported_operation_atoms_count=supported,
        presence_only_operation_atoms_count=presence_only,
        insufficient_transformation_evidence_operation_atoms_count=insufficient,
        rejected_noop_equivalent_operation_atoms_count=rejected_noop,
        schema_invalid_atoms_count=0 if annotation_status == "schema_valid" else expected,
        semantic_guard_atoms_count=semantic_guards,
        boundary_notes=boundary_notes,
    )


def _export(tmp_path: Path, rows: tuple[POCRDiagnosticRow, ...]) -> list[dict[str, str]]:
    path = tmp_path / "results" / "run" / "pocr" / "stage_b" / "pocr_stage_b_row_metrics.csv"
    export_stage_b_row_metrics(path, rows)
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_stage_b_metrics_schema_valid_row_has_partial_oc_i(tmp_path: Path) -> None:
    [row] = _export(tmp_path, (_row(tmp_path=tmp_path, expected=4, supported=1),))

    assert row["oc_i"] == "0.250000000000"
    assert row["oc_i_fail_closed"] == "0.250000000000"
    assert row["fail_closed_status"] == "none"
    assert row["stage_b_supported_operation_atoms"] == "1"
    assert row["expected_operation_atoms"] == "4"


def test_stage_b_metrics_noop_zero_supported_atoms(tmp_path: Path) -> None:
    [row] = _export(
        tmp_path,
        (
            _row(
                tmp_path=tmp_path,
                case_id="CONS_0005",
                stage_b_status="presence_only",
                expected=3,
                supported=0,
                presence_only=2,
            ),
        ),
    )

    assert row["oc_i"] == "0.000000000000"
    assert row["oc_i_fail_closed"] == "0.000000000000"
    assert row["presence_only_operation_atoms"] == "2"
    assert row["fail_closed_status"] == "none"


def test_stage_b_metrics_malformed_annotation_fails_closed(tmp_path: Path) -> None:
    [row] = _export(
        tmp_path,
        (
            _row(
                tmp_path=tmp_path,
                case_id="PORT_0003",
                annotation_status="malformed_json",
                stage_b_status="schema_invalid",
                expected=2,
                supported=0,
                boundary_notes="malformed_json provider output failed closed",
            ),
        ),
    )

    assert row["fail_closed_status"] == "malformed_json"
    assert row["oc_i"] == ""
    assert row["oc_i_fail_closed"] == "0"
    assert row["pocr_planned_denominator_member"] == "true"
    assert row["pocr_candidate_denominator_member"] == "true"


def test_stage_b_metrics_provider_failed_fails_closed(tmp_path: Path) -> None:
    [row] = _export(
        tmp_path,
        (
            _row(
                tmp_path=tmp_path,
                case_id="PERF_0013",
                annotation_status="provider_call_failed",
                stage_b_status="schema_invalid",
                expected=2,
                supported=0,
                boundary_notes="provider_call_failed",
            ),
        ),
    )

    assert row["fail_closed_status"] == "provider_call_failed"
    assert row["oc_i_fail_closed"] == "0"


def test_stage_b_metrics_route_mismatch_fails_closed(tmp_path: Path) -> None:
    [row] = _export(
        tmp_path,
        (
            _row(
                tmp_path=tmp_path,
                case_id="LONGTAIL_0011",
                annotation_status="schema_invalid",
                stage_b_status="schema_invalid",
                expected=2,
                supported=0,
                boundary_notes="route_mismatch",
            ),
        ),
    )

    assert row["route_mismatch"] == "true"
    assert row["fail_closed_status"] == "route_mismatch"
    assert row["oc_i_fail_closed"] == "0"


def test_stage_b_metrics_candidate_mismatch_fails_closed(tmp_path: Path) -> None:
    [row] = _export(
        tmp_path,
        (
            _row(
                tmp_path=tmp_path,
                case_id="PERF_0017",
                annotation_status="schema_invalid",
                stage_b_status="schema_invalid",
                expected=2,
                supported=0,
                boundary_notes="candidate_mismatch",
            ),
        ),
    )

    assert row["candidate_mismatch"] == "true"
    assert row["fail_closed_status"] == "candidate_mismatch"
    assert row["oc_i_fail_closed"] == "0"


def test_stage_b_metrics_no_expected_operation_atoms_are_not_applicable(tmp_path: Path) -> None:
    [row] = _export(
        tmp_path,
        (
            _row(
                tmp_path=tmp_path,
                case_id="CONS_0007",
                expected=0,
                supported=0,
                semantic_guards=1,
            ),
        ),
    )

    assert row["oc_i"] == "NA"
    assert row["oc_i_fail_closed"] == "NA"
    assert row["not_applicable_reason"] == "not_applicable_no_expected_operation_atoms"
    assert row["pocr_planned_denominator_member"] == "false"
    assert row["pocr_candidate_denominator_member"] == "false"


def test_stage_b_metrics_curated_stays_false_and_boundaries_hold(tmp_path: Path) -> None:
    [row] = _export(tmp_path, (_row(tmp_path=tmp_path),))

    assert row["pocr_curated_denominator_member"] == "false"
    assert row["diagnostic_only"] == "true"
    assert row["official_pocr_computed"] == "false"
    assert row["route_level_pocr_aggregated"] == "false"
    assert row["paper_metric_promoted"] == "false"


def test_stage_b_metrics_required_columns_and_candidate_sha(tmp_path: Path) -> None:
    candidate = _candidate(tmp_path, "PERF_0052")
    row = POCRDiagnosticRow(
        run_id="pocr_stage_b_metrics_test",
        case_id="PERF_0052",
        pool="PERF",
        engine="postgres",
        method_id="method",
        route_id="route",
        candidate_path=candidate.as_posix(),
        candidate_present=True,
        skill_present=True,
        annotation_status="schema_valid",
        stage_b_status="transformation_evidence_partial",
        expected_operation_atoms_count=2,
        stage_a_implemented_operation_atoms_count=1,
        transformation_supported_operation_atoms_count=1,
        presence_only_operation_atoms_count=0,
        insufficient_transformation_evidence_operation_atoms_count=0,
        rejected_noop_equivalent_operation_atoms_count=0,
        schema_invalid_atoms_count=0,
        semantic_guard_atoms_count=0,
    )

    [exported] = _export(tmp_path, (row,))

    assert set(stage_b_row_metric_fields()).issubset(exported)
    assert exported["candidate_sha256"] == hashlib.sha256(candidate.read_bytes()).hexdigest()
