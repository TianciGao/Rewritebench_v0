from pathlib import Path

import pytest

from sql_rewrite_bench.pocr.annotation_client import AnnotationClientConfig, build_annotation_client
from sql_rewrite_bench.pocr.annotation_schema import ANNOTATION_SCHEMA_VERSION, annotation_from_mapping
from sql_rewrite_bench.pocr.evidence_validation import SyntheticEvidenceRef, validate_stage_b
from sql_rewrite_bench.pocr.pocr_row import POCRRowDraft
from sql_rewrite_bench.pocr.skills_parser import parse_skills_text


SAMPLE_SKILLS = """# Baseline Rewrite Audit Skill

## Scope

- case_id: `CASE_0003`
- pool: `PORT`

## Atom Protocol

| atom | category | type | risk | weight | requirement |
|---|---|---|---|---:|---|
| O1 | `operation_atom` | `dialect_normalization` | medium | 1.0 | Candidate normalizes dialect-specific syntax. |
| S1 | `semantic_guard_atom` | `null_preservation` | high | 1.0 | Candidate preserves null behavior. |

## Required Candidate Annotation Shape

Return JSON.

## Review Boundaries

- Parse-only.
"""


def _contract():
    result = parse_skills_text(
        SAMPLE_SKILLS,
        skills_path=Path("cases/PORT/CASE_0003/skills.md"),
        expected_case_id="CASE_0003",
        expected_pool="PORT",
    )
    assert result.contract is not None
    return result.contract


def _payload():
    return {
        "case_id": "CASE_0003",
        "pool": "PORT",
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
                "evidence_refs": [],
                "confidence": "medium",
            },
            {
                "atom_id": "S1",
                "atom_type": "semantic_guard_atom",
                "expected": True,
                "observed_status": "implemented",
                "rationale_short": "Fixture rationale, not independent evidence.",
                "evidence_refs": [],
                "confidence": "medium",
            },
        ],
    }


def test_stage_b_fails_closed_without_independent_evidence() -> None:
    contract = _contract()
    result = validate_stage_b(contract, annotation_from_mapping(_payload()))

    assert result.schema_valid
    assert result.stage_b_status == "insufficient_evidence"
    assert {atom.evidence_status for atom in result.atom_results} == {"insufficient_evidence"}
    assert result.validated_operation_atoms_count == 0


def test_stage_b_rejects_invalid_atom_id() -> None:
    payload = _payload()
    payload["atoms"][0]["atom_id"] = "BAD"
    result = validate_stage_b(_contract(), annotation_from_mapping(payload))

    assert not result.schema_valid
    assert "atom_not_in_contract" in {issue.code for issue in result.issues}
    assert "atom_not_in_contract" in {atom.evidence_status for atom in result.atom_results}


def test_stage_b_reports_duplicate_and_missing_atom_judgments() -> None:
    payload = _payload()
    payload["atoms"][1]["atom_id"] = "O1"
    payload["atoms"][1]["atom_type"] = "operation_atom"
    result = validate_stage_b(_contract(), annotation_from_mapping(payload))

    codes = {issue.code for issue in result.issues}
    assert "duplicate_atom_judgment" in codes
    assert "missing_atom_judgment" in codes
    assert not result.schema_valid


def test_stage_b_fixture_evidence_validates_only_matching_operation_atom() -> None:
    payload = _payload()
    payload["atoms"][0]["evidence_refs"] = ["synthetic:O1"]
    payload["atoms"][1]["evidence_refs"] = ["synthetic:S1"]
    annotation = annotation_from_mapping(payload)

    result = validate_stage_b(
        _contract(),
        annotation,
        synthetic_evidence_refs=(
            SyntheticEvidenceRef(evidence_id="synthetic:O1", atom_id="O1"),
            SyntheticEvidenceRef(evidence_id="synthetic:S1", atom_id="S1"),
        ),
    )
    row = POCRRowDraft.from_stage_b(_contract(), result, denominator_eligible=True)

    assert result.stage_b_status == "partial_validated"
    assert result.validated_operation_atoms_count == 1
    assert row.validated_operation_atoms_count == 1
    assert row.expected_operation_atoms_count == 1
    assert row.fixture_operation_ratio() == 1.0
    assert row.official_metric is False


def test_semantic_guard_is_not_counted_as_operation_numerator() -> None:
    payload = _payload()
    payload["atoms"][1]["evidence_refs"] = ["synthetic:S1"]
    result = validate_stage_b(
        _contract(),
        annotation_from_mapping(payload),
        synthetic_evidence_refs=(SyntheticEvidenceRef(evidence_id="synthetic:S1", atom_id="S1"),),
    )

    assert any(atom.atom_type == "semantic_guard_atom" and atom.evidence_status == "validated" for atom in result.atom_results)
    assert result.validated_operation_atoms_count == 0


def test_stage_b_rejects_llm_rationale_and_speedup_evidence_refs() -> None:
    payload = _payload()
    payload["atoms"][0]["evidence_refs"] = ["llm_rationale:O1"]
    payload["atoms"][1]["evidence_refs"] = ["speedup:S1"]
    result = validate_stage_b(_contract(), annotation_from_mapping(payload))

    assert {atom.evidence_status for atom in result.atom_results} == {"rejected"}


def test_fake_annotation_client_returns_fixture() -> None:
    client = build_annotation_client(AnnotationClientConfig(mode="fake"), fixture_response=_payload())

    annotation = client.annotate("strict prompt")

    assert annotation.case_id == "CASE_0003"
    assert annotation.route_id == "fixture_route"


def test_live_annotation_client_fails_closed_without_gate() -> None:
    with pytest.raises(RuntimeError, match="disabled"):
        build_annotation_client(AnnotationClientConfig(mode="live", allow_live=False))
