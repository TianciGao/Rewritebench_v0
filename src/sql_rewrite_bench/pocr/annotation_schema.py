"""Structured Stage A annotation schema for POCR candidate rows.

This module defines offline-validated data structures only. It does not call
LLMs, judge candidate SQL by itself, or compute Positive Operation Coverage
Rate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Mapping

from sql_rewrite_bench.pocr.models import AtomCategory, SkillContract, SkillValidationIssue

ANNOTATION_SCHEMA_VERSION = "pocr_candidate_annotation_v1"

ObservedStatus = Literal["implemented", "not_implemented", "contradicted", "unclear", "not_applicable"]
Confidence = Literal["high", "medium", "low"]

ALLOWED_OBSERVED_STATUSES = {
    "implemented",
    "not_implemented",
    "contradicted",
    "unclear",
    "not_applicable",
}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}


@dataclass(frozen=True)
class AtomJudgment:
    """One candidate-level judgment for one atom from skills.md."""

    atom_id: str
    atom_type: AtomCategory
    expected: bool
    observed_status: str
    rationale_short: str
    evidence_refs: tuple[str, ...]
    confidence: str


@dataclass(frozen=True)
class CandidateAnnotation:
    """Strict Stage A annotation object for one method candidate row."""

    case_id: str
    pool: str
    engine: str
    method_id: str
    route_id: str
    candidate_id: str | None
    candidate_path: str | None
    annotation_schema_version: str
    atoms: tuple[AtomJudgment, ...]

    @property
    def candidate_ref(self) -> str | None:
        return self.candidate_id or self.candidate_path


def annotation_from_mapping(raw: Mapping[str, Any]) -> CandidateAnnotation:
    """Convert a JSON-like mapping to a typed annotation object.

    The conversion is intentionally strict about top-level shape and scalar
    field types. Contract-specific checks, such as atom membership, are handled
    by :func:`validate_candidate_annotation`.
    """

    atoms_raw = raw.get("atoms")
    if not isinstance(atoms_raw, list):
        raise ValueError("annotation field 'atoms' must be a list")

    candidate_id = raw.get("candidate_id")
    candidate_path = raw.get("candidate_path")
    if candidate_id is not None and not isinstance(candidate_id, str):
        raise ValueError("annotation field 'candidate_id' must be a string when present")
    if candidate_path is not None and not isinstance(candidate_path, str):
        raise ValueError("annotation field 'candidate_path' must be a string when present")

    atoms = tuple(_atom_judgment_from_mapping(atom) for atom in atoms_raw)
    return CandidateAnnotation(
        case_id=_required_str(raw, "case_id"),
        pool=_required_str(raw, "pool"),
        engine=_required_str(raw, "engine"),
        method_id=_required_str(raw, "method_id"),
        route_id=_required_str(raw, "route_id"),
        candidate_id=candidate_id,
        candidate_path=candidate_path,
        annotation_schema_version=_required_str(raw, "annotation_schema_version"),
        atoms=atoms,
    )


def annotation_to_json_dict(annotation: CandidateAnnotation) -> dict[str, object]:
    """Return a JSON-serializable dict preserving the strict schema fields."""

    payload: dict[str, object] = {
        "case_id": annotation.case_id,
        "pool": annotation.pool,
        "engine": annotation.engine,
        "method_id": annotation.method_id,
        "route_id": annotation.route_id,
        "annotation_schema_version": annotation.annotation_schema_version,
        "atoms": [
            {
                "atom_id": atom.atom_id,
                "atom_type": atom.atom_type,
                "expected": atom.expected,
                "observed_status": atom.observed_status,
                "rationale_short": atom.rationale_short,
                "evidence_refs": list(atom.evidence_refs),
                "confidence": atom.confidence,
            }
            for atom in annotation.atoms
        ],
    }
    if annotation.candidate_id is not None:
        payload["candidate_id"] = annotation.candidate_id
    if annotation.candidate_path is not None:
        payload["candidate_path"] = annotation.candidate_path
    return payload


def validate_candidate_annotation(
    annotation: CandidateAnnotation,
    contract: SkillContract,
    *,
    expected_engine: str | None = None,
    expected_method_id: str | None = None,
    expected_route_id: str | None = None,
) -> tuple[SkillValidationIssue, ...]:
    """Validate one Stage A annotation against the case-local skill contract.

    This schema validation is not evidence validation and does not determine a
    POCR numerator. It only checks that the candidate-level JSON is well formed
    and covers the atom IDs defined in skills.md.
    """

    issues: list[SkillValidationIssue] = []
    atom_by_id = {atom.atom_id: atom for atom in contract.atoms}
    seen: set[str] = set()

    if annotation.annotation_schema_version != ANNOTATION_SCHEMA_VERSION:
        issues.append(_issue(contract, "unsupported_annotation_schema_version", annotation.annotation_schema_version))
    if annotation.case_id != contract.case_id:
        issues.append(_issue(contract, "annotation_case_id_mismatch", annotation.case_id))
    if annotation.pool != contract.pool:
        issues.append(_issue(contract, "annotation_pool_mismatch", annotation.pool))
    if expected_engine is not None and annotation.engine != expected_engine:
        issues.append(_issue(contract, "annotation_engine_mismatch", annotation.engine))
    if expected_method_id is not None and annotation.method_id != expected_method_id:
        issues.append(_issue(contract, "annotation_method_id_mismatch", annotation.method_id))
    if expected_route_id is not None and annotation.route_id != expected_route_id:
        issues.append(_issue(contract, "annotation_route_id_mismatch", annotation.route_id))
    if not annotation.candidate_ref:
        issues.append(_issue(contract, "missing_candidate_reference", "candidate_id or candidate_path is required"))

    for atom in annotation.atoms:
        if atom.atom_id in seen:
            issues.append(_issue(contract, "duplicate_atom_judgment", atom.atom_id))
        seen.add(atom.atom_id)
        expected_atom = atom_by_id.get(atom.atom_id)
        if expected_atom is None:
            issues.append(_issue(contract, "atom_not_in_contract", atom.atom_id))
            continue
        if atom.atom_type != expected_atom.category:
            issues.append(
                _issue(
                    contract,
                    "atom_type_mismatch",
                    f"{atom.atom_id}: {atom.atom_type} != {expected_atom.category}",
                )
            )
        if atom.expected is not True:
            issues.append(_issue(contract, "atom_expected_not_true", atom.atom_id))
        if atom.observed_status not in ALLOWED_OBSERVED_STATUSES:
            issues.append(_issue(contract, "invalid_observed_status", f"{atom.atom_id}: {atom.observed_status}"))
        if atom.confidence not in ALLOWED_CONFIDENCE:
            issues.append(_issue(contract, "invalid_confidence", f"{atom.atom_id}: {atom.confidence}"))
        if not atom.rationale_short.strip():
            issues.append(_issue(contract, "missing_rationale_short", atom.atom_id))
        for evidence_ref in atom.evidence_refs:
            if not evidence_ref.strip():
                issues.append(_issue(contract, "malformed_evidence_ref", atom.atom_id))

    missing = sorted(set(atom_by_id) - seen)
    for atom_id in missing:
        issues.append(_issue(contract, "missing_atom_judgment", atom_id))

    return tuple(issues)


def _atom_judgment_from_mapping(raw: object) -> AtomJudgment:
    if not isinstance(raw, Mapping):
        raise ValueError("annotation atom entries must be objects")
    evidence_refs = raw.get("evidence_refs")
    if not isinstance(evidence_refs, list) or not all(isinstance(item, str) for item in evidence_refs):
        raise ValueError("atom field 'evidence_refs' must be a list of strings")
    expected = raw.get("expected")
    if not isinstance(expected, bool):
        raise ValueError("atom field 'expected' must be a boolean")
    return AtomJudgment(
        atom_id=_required_str(raw, "atom_id"),
        atom_type=_required_str(raw, "atom_type"),  # type: ignore[arg-type]
        expected=expected,
        observed_status=_required_str(raw, "observed_status"),
        rationale_short=_required_str(raw, "rationale_short"),
        evidence_refs=tuple(evidence_refs),
        confidence=_required_str(raw, "confidence"),
    )


def _required_str(raw: Mapping[str, Any], field_name: str) -> str:
    value = raw.get(field_name)
    if not isinstance(value, str) or not value:
        raise ValueError(f"annotation field {field_name!r} must be a non-empty string")
    return value


def _issue(contract: SkillContract, code: str, detail: str) -> SkillValidationIssue:
    return SkillValidationIssue(
        case_id=contract.case_id,
        pool=contract.pool,
        skills_path=contract.skills_path,
        code=code,
        message=detail,
    )
