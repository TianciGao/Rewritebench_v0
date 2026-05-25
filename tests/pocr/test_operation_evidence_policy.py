from pathlib import Path

from sql_rewrite_bench.pocr.annotation_schema import ANNOTATION_SCHEMA_VERSION, annotation_from_mapping
from sql_rewrite_bench.pocr.operation_evidence_policy import validate_transformation_stage_b
from sql_rewrite_bench.pocr.skills_parser import parse_skills_text


SAMPLE_SKILLS = """# Baseline Rewrite Audit Skill

## Scope

- case_id: `CASE_0005`
- pool: `PERF`

## Atom Protocol

| atom | category | type | risk | weight | requirement |
|---|---|---|---|---:|---|
| O1 | `operation_atom` | `predicate_introduction` | medium | 1.0 | Candidate introduces the safe predicate. |
| S1 | `semantic_guard_atom` | `row_preservation` | high | 1.0 | Candidate preserves rows. |

## Required Candidate Annotation Shape

Return JSON.

## Review Boundaries

- Parse-only.
"""


def _contract():
    result = parse_skills_text(
        SAMPLE_SKILLS,
        skills_path=Path("cases/PERF/CASE_0005/skills.md"),
        expected_case_id="CASE_0005",
        expected_pool="PERF",
    )
    assert result.contract is not None
    return result.contract


def _payload(*, op_refs: list[str] | None = None, guard_refs: list[str] | None = None, observed: str = "implemented"):
    return {
        "case_id": "CASE_0005",
        "pool": "PERF",
        "engine": "postgres",
        "method_id": "fixture_method",
        "route_id": "fixture_route",
        "candidate_id": "candidate_001",
        "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
        "atoms": [
            {
                "atom_id": "O1",
                "atom_type": "operation_atom",
                "expected": True,
                "observed_status": observed,
                "rationale_short": "Fixture rationale, not evidence.",
                "evidence_refs": op_refs or [],
                "confidence": "medium",
            },
            {
                "atom_id": "S1",
                "atom_type": "semantic_guard_atom",
                "expected": True,
                "observed_status": "implemented",
                "rationale_short": "Fixture rationale, not evidence.",
                "evidence_refs": guard_refs or [],
                "confidence": "medium",
            },
        ],
    }


def _validate(payload: dict[str, object], *, source: str = "select * from t;", candidate: str = "select * from t where rn = 1;"):
    return validate_transformation_stage_b(
        _contract(),
        annotation_from_mapping(payload),
        source_sql=source,
        candidate_sql=candidate,
        positive_sql="select * from t where rn = 1;",
    )


def test_candidate_sql_span_alone_is_presence_only_not_transformation_supported() -> None:
    result = _validate(_payload(op_refs=["candidate_sql_span:where rn = 1"]))

    assert result.presence_only_operation_atoms_count == 1
    assert result.transformation_supported_operation_atoms_count == 0


def test_source_sql_span_alone_is_not_operation_coverage_evidence() -> None:
    result = _validate(_payload(op_refs=["source_sql_span:from t"]))

    assert result.presence_only_operation_atoms_count == 1
    assert result.transformation_supported_operation_atoms_count == 0


def test_positive_sql_span_alone_is_not_operation_coverage_evidence() -> None:
    result = _validate(_payload(op_refs=["positive_sql_span:where rn = 1"]))

    assert result.presence_only_operation_atoms_count == 1
    assert result.transformation_supported_operation_atoms_count == 0


def test_candidate_span_plus_diff_changed_can_support_transformation() -> None:
    result = _validate(
        _payload(op_refs=["candidate_sql_span:where rn = 1", "source_candidate_diff:changed"])
    )

    assert result.transformation_supported_operation_atoms_count == 1


def test_positive_aligned_candidate_span_plus_diff_changed_can_support_transformation() -> None:
    result = _validate(
        _payload(op_refs=["positive_sql_span:where rn = 1", "source_candidate_diff:changed"])
    )

    assert result.transformation_supported_operation_atoms_count == 1


def test_normalized_noop_candidate_is_rejected_or_presence_only() -> None:
    result = _validate(
        _payload(op_refs=["source_candidate_diff:changed"]),
        source="select * from t;",
        candidate="SELECT * FROM t",
    )

    assert result.rejected_noop_equivalent_operation_atoms_count == 1
    assert result.transformation_supported_operation_atoms_count == 0


def test_semantic_guard_atom_not_counted_as_operation_numerator() -> None:
    result = _validate(
        _payload(guard_refs=["candidate_sql_span:where rn = 1", "source_candidate_diff:changed"])
    )

    assert result.transformation_supported_operation_atoms_count == 0
    assert any(
        atom.atom_type == "semantic_guard_atom" and atom.evidence_status == "validated_static_span"
        for atom in result.atom_results
    )


def test_invalid_atom_ids_fail_closed() -> None:
    payload = _payload(op_refs=["candidate_sql_span:where rn = 1", "source_candidate_diff:changed"])
    payload["atoms"][0]["atom_id"] = "BAD"

    result = _validate(payload)

    assert not result.schema_valid
    assert result.stage_b_status == "schema_invalid"
    assert result.transformation_supported_operation_atoms_count == 0


def test_malformed_or_missing_schema_remains_schema_invalid() -> None:
    payload = _payload()
    payload["atoms"][1]["atom_id"] = "O1"

    result = _validate(payload)

    assert not result.schema_valid
    assert result.stage_b_status == "schema_invalid"


def test_unsupported_evidence_refs_are_rejected() -> None:
    result = _validate(_payload(op_refs=["candidate_sql:where rn = 1"]))

    assert {atom.evidence_status for atom in result.atom_results if atom.atom_type == "operation_atom"} == {"invalid_ref"}
    assert result.transformation_supported_operation_atoms_count == 0
