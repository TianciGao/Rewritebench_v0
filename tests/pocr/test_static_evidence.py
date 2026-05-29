from pathlib import Path

from sql_rewrite_bench.pocr.annotation_schema import ANNOTATION_SCHEMA_VERSION, annotation_from_mapping
from sql_rewrite_bench.pocr.skills_parser import parse_skills_text
from sql_rewrite_bench.pocr.static_evidence import validate_static_stage_b


SAMPLE_SKILLS = """# Baseline Rewrite Audit Skill

## Scope

- case_id: `CASE_0004`
- pool: `PERF`

## Atom Protocol

| atom | category | type | risk | weight | requirement |
|---|---|---|---|---:|---|
| O1 | `operation_atom` | `projection_simplification` | medium | 1.0 | Candidate keeps one projected column. |
| S1 | `semantic_guard_atom` | `row_preservation` | high | 1.0 | Candidate preserves rows. |

## Required Candidate Annotation Shape

Return JSON.

## Review Boundaries

- Parse-only.
"""


def _contract():
    result = parse_skills_text(
        SAMPLE_SKILLS,
        skills_path=Path("cases/PERF/CASE_0004/skills.md"),
        expected_case_id="CASE_0004",
        expected_pool="PERF",
    )
    assert result.contract is not None
    return result.contract


def _payload(*, op_refs: list[str] | None = None, guard_refs: list[str] | None = None):
    return {
        "case_id": "CASE_0004",
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
                "observed_status": "implemented",
                "rationale_short": "Fixture rationale, not independent evidence.",
                "evidence_refs": op_refs or [],
                "confidence": "medium",
            },
            {
                "atom_id": "S1",
                "atom_type": "semantic_guard_atom",
                "expected": True,
                "observed_status": "implemented",
                "rationale_short": "Fixture rationale, not independent evidence.",
                "evidence_refs": guard_refs or [],
                "confidence": "medium",
            },
        ],
    }


def _validate(payload: dict[str, object]):
    return validate_static_stage_b(
        _contract(),
        annotation_from_mapping(payload),
        source_sql="select id, name from accounts;",
        candidate_sql="select name from accounts;",
        positive_sql="select name from accounts;",
    )


def test_static_evidence_validates_candidate_sql_span() -> None:
    result = _validate(_payload(op_refs=["candidate_sql_span:select name from accounts"]))

    assert result.stage_b_status == "static_evidence_partial"
    assert result.static_validated_operation_atoms_count == 1
    assert result.static_rejected_operation_atoms_count == 0
    assert any(atom.evidence_status == "validated_static_span" for atom in result.atom_results)


def test_static_evidence_rejects_missing_candidate_sql_span() -> None:
    result = _validate(_payload(op_refs=["candidate_sql_span:where missing = true"]))

    assert result.stage_b_status == "static_evidence_rejected"
    assert result.static_validated_operation_atoms_count == 0
    assert result.static_rejected_operation_atoms_count == 1


def test_static_evidence_rejects_invalid_ref_format() -> None:
    result = _validate(_payload(op_refs=["candidate_sql: select name from accounts"]))

    assert result.stage_b_status == "static_evidence_rejected"
    assert {atom.evidence_status for atom in result.atom_results if atom.atom_id == "O1"} == {
        "rejected_invalid_ref"
    }


def test_static_evidence_no_refs_remains_insufficient() -> None:
    result = _validate(_payload())

    assert result.stage_b_status == "insufficient_evidence"
    assert result.static_validated_operation_atoms_count == 0


def test_static_evidence_invalid_atom_id_is_schema_invalid() -> None:
    payload = _payload(op_refs=["candidate_sql_span:select name"])
    payload["atoms"][0]["atom_id"] = "BAD"
    result = _validate(payload)

    assert not result.schema_valid
    assert result.stage_b_status == "schema_invalid"
    assert "atom_not_in_contract" in {atom.evidence_status for atom in result.atom_results}


def test_static_evidence_duplicate_and_missing_atoms_are_schema_invalid() -> None:
    payload = _payload()
    payload["atoms"][1]["atom_id"] = "O1"
    payload["atoms"][1]["atom_type"] = "operation_atom"
    result = _validate(payload)

    assert not result.schema_valid
    assert result.stage_b_status == "schema_invalid"
    assert {"duplicate_atom_judgment", "missing_atom_judgment"}.issubset({issue.code for issue in result.issues})


def test_semantic_guard_static_span_not_counted_as_operation_numerator() -> None:
    result = _validate(_payload(guard_refs=["candidate_sql_span:select name from accounts"]))

    assert result.stage_b_status == "static_evidence_partial"
    assert result.static_validated_operation_atoms_count == 0
    assert any(
        atom.atom_type == "semantic_guard_atom" and atom.evidence_status == "validated_static_span"
        for atom in result.atom_results
    )


def test_candidate_token_span_is_whitespace_and_case_insensitive() -> None:
    result = _validate(_payload(op_refs=["candidate_token_span:SELECT   NAME FROM ACCOUNTS"]))

    assert result.static_validated_operation_atoms_count == 1


def test_source_candidate_diff_changed_is_diagnostic_only() -> None:
    result = _validate(_payload(op_refs=["source_candidate_diff:changed"]))

    assert result.static_validated_operation_atoms_count == 1
