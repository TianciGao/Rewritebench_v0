from pathlib import Path

import pytest

from sql_rewrite_bench.pocr.annotation_schema import (
    ANNOTATION_SCHEMA_VERSION,
    annotation_from_mapping,
    validate_candidate_annotation,
)
from sql_rewrite_bench.pocr.skills_parser import parse_skills_text


SAMPLE_SKILLS = """# Baseline Rewrite Audit Skill

## Scope

- case_id: `CASE_0001`
- pool: `PERF`

## Atom Protocol

| atom | category | type | risk | weight | requirement |
|---|---|---|---|---:|---|
| A1 | `operation_atom` | `join_elimination` | medium | 1.0 | Candidate removes redundant join. |
| G1 | `semantic_guard_atom` | `null_preservation` | high | 1.0 | Candidate preserves null behavior. |

## Required Candidate Annotation Shape

Return JSON.

## Review Boundaries

- Parse-only.
"""


def _contract():
    result = parse_skills_text(
        SAMPLE_SKILLS,
        skills_path=Path("cases/PERF/CASE_0001/skills.md"),
        expected_case_id="CASE_0001",
        expected_pool="PERF",
    )
    assert result.contract is not None
    return result.contract


def _annotation_payload(**overrides):
    payload = {
        "case_id": "CASE_0001",
        "pool": "PERF",
        "engine": "postgres",
        "method_id": "fixture_method",
        "route_id": "fixture_route",
        "candidate_id": "candidate_001",
        "annotation_schema_version": ANNOTATION_SCHEMA_VERSION,
        "atoms": [
            {
                "atom_id": "A1",
                "atom_type": "operation_atom",
                "expected": True,
                "observed_status": "implemented",
                "rationale_short": "The candidate removes the redundant join.",
                "evidence_refs": [],
                "confidence": "medium",
            },
            {
                "atom_id": "G1",
                "atom_type": "semantic_guard_atom",
                "expected": True,
                "observed_status": "unclear",
                "rationale_short": "No independent evidence is available in this fixture.",
                "evidence_refs": [],
                "confidence": "low",
            },
        ],
    }
    payload.update(overrides)
    return payload


def test_valid_annotation_schema_covers_contract_atoms() -> None:
    annotation = annotation_from_mapping(_annotation_payload())

    issues = validate_candidate_annotation(annotation, _contract())

    assert issues == ()


def test_invalid_atom_id_is_reported() -> None:
    payload = _annotation_payload()
    payload["atoms"][0]["atom_id"] = "NOT_IN_CONTRACT"
    annotation = annotation_from_mapping(payload)

    codes = {issue.code for issue in validate_candidate_annotation(annotation, _contract())}

    assert "atom_not_in_contract" in codes
    assert "missing_atom_judgment" in codes


def test_duplicate_atom_id_is_reported() -> None:
    payload = _annotation_payload()
    payload["atoms"][1]["atom_id"] = "A1"
    payload["atoms"][1]["atom_type"] = "operation_atom"
    annotation = annotation_from_mapping(payload)

    codes = {issue.code for issue in validate_candidate_annotation(annotation, _contract())}

    assert "duplicate_atom_judgment" in codes
    assert "missing_atom_judgment" in codes


def test_missing_atom_judgment_is_reported() -> None:
    payload = _annotation_payload()
    payload["atoms"] = payload["atoms"][:1]
    annotation = annotation_from_mapping(payload)

    codes = {issue.code for issue in validate_candidate_annotation(annotation, _contract())}

    assert "missing_atom_judgment" in codes


def test_malformed_json_shape_fails_strict_conversion() -> None:
    payload = _annotation_payload(atoms={"A1": "implemented"})

    with pytest.raises(ValueError, match="atoms"):
        annotation_from_mapping(payload)
