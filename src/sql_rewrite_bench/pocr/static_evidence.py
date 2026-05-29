"""Conservative static evidence checks for POCR Stage B diagnostics."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from sql_rewrite_bench.pocr.annotation_schema import CandidateAnnotation, validate_candidate_annotation
from sql_rewrite_bench.pocr.models import AtomCategory, SkillContract, SkillValidationIssue

StaticEvidenceStatus = Literal[
    "validated_static_span",
    "rejected_missing_span",
    "rejected_invalid_ref",
    "insufficient_evidence",
    "schema_invalid",
    "atom_not_in_contract",
]

SUPPORTED_STATIC_REF_PREFIXES = {
    "candidate_sql_span",
    "source_sql_span",
    "positive_sql_span",
    "candidate_token_span",
    "source_candidate_diff",
}


@dataclass(frozen=True)
class StaticAtomEvidenceValidation:
    atom_id: str
    atom_type: AtomCategory | str
    observed_status: str
    evidence_status: StaticEvidenceStatus
    evidence_refs: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class StaticStageBValidationResult:
    case_id: str | None
    pool: str | None
    engine: str
    method_id: str
    route_id: str
    schema_valid: bool
    issues: tuple[SkillValidationIssue, ...]
    atom_results: tuple[StaticAtomEvidenceValidation, ...]

    @property
    def stage_b_status(self) -> str:
        if not self.schema_valid:
            return "schema_invalid"
        if any(atom.evidence_status == "validated_static_span" for atom in self.atom_results):
            return "static_evidence_partial"
        if any(atom.evidence_status.startswith("rejected_") for atom in self.atom_results):
            return "static_evidence_rejected"
        return "insufficient_evidence"

    @property
    def static_validated_operation_atoms_count(self) -> int:
        return sum(
            1
            for atom in self.atom_results
            if atom.atom_type == "operation_atom" and atom.evidence_status == "validated_static_span"
        )

    @property
    def static_rejected_operation_atoms_count(self) -> int:
        return sum(
            1
            for atom in self.atom_results
            if atom.atom_type == "operation_atom" and atom.evidence_status.startswith("rejected_")
        )


def validate_static_stage_b(
    contract: SkillContract,
    annotation: CandidateAnnotation,
    *,
    source_sql: str,
    candidate_sql: str,
    positive_sql: str | None = None,
    negative_sql: str | None = None,
) -> StaticStageBValidationResult:
    """Validate explicit static evidence refs without computing POCR.

    The static validator confirms only cited spans or coarse source/candidate
    text differences. It does not infer an atom from SQL text, LLM rationale,
    checker exactness, taxonomy tags, speedup, or runtime behavior.
    """

    del negative_sql  # reserved for a later explicit evidence contract
    issues = validate_candidate_annotation(annotation, contract)
    schema_valid = not any(issue.severity == "error" for issue in issues)
    contract_atom_ids = {atom.atom_id for atom in contract.atoms}
    atom_results: list[StaticAtomEvidenceValidation] = []

    for atom in annotation.atoms:
        if atom.atom_id not in contract_atom_ids:
            atom_results.append(
                StaticAtomEvidenceValidation(
                    atom_id=atom.atom_id,
                    atom_type=atom.atom_type,
                    observed_status=atom.observed_status,
                    evidence_status="atom_not_in_contract",
                    evidence_refs=atom.evidence_refs,
                    reason="atom ID is not present in skills.md",
                )
            )
            continue
        if not schema_valid:
            atom_results.append(
                StaticAtomEvidenceValidation(
                    atom_id=atom.atom_id,
                    atom_type=atom.atom_type,
                    observed_status=atom.observed_status,
                    evidence_status="schema_invalid",
                    evidence_refs=atom.evidence_refs,
                    reason="annotation schema validation failed",
                )
            )
            continue
        status, reason = _validate_atom_static_refs(
            atom.evidence_refs,
            source_sql=source_sql,
            candidate_sql=candidate_sql,
            positive_sql=positive_sql,
        )
        atom_results.append(
            StaticAtomEvidenceValidation(
                atom_id=atom.atom_id,
                atom_type=atom.atom_type,
                observed_status=atom.observed_status,
                evidence_status=status,
                evidence_refs=atom.evidence_refs,
                reason=reason,
            )
        )

    return StaticStageBValidationResult(
        case_id=annotation.case_id,
        pool=annotation.pool,
        engine=annotation.engine,
        method_id=annotation.method_id,
        route_id=annotation.route_id,
        schema_valid=schema_valid,
        issues=issues,
        atom_results=tuple(atom_results),
    )


def _validate_atom_static_refs(
    evidence_refs: tuple[str, ...],
    *,
    source_sql: str,
    candidate_sql: str,
    positive_sql: str | None,
) -> tuple[StaticEvidenceStatus, str]:
    if not evidence_refs:
        return "insufficient_evidence", "no explicit static evidence refs were provided"

    saw_missing = False
    saw_invalid = False
    for evidence_ref in evidence_refs:
        status, reason = _validate_one_ref(
            evidence_ref,
            source_sql=source_sql,
            candidate_sql=candidate_sql,
            positive_sql=positive_sql,
        )
        if status == "validated_static_span":
            return status, reason
        if status == "rejected_invalid_ref":
            saw_invalid = True
        elif status == "rejected_missing_span":
            saw_missing = True

    if saw_invalid:
        return "rejected_invalid_ref", "no supported static ref validated; at least one ref was invalid"
    if saw_missing:
        return "rejected_missing_span", "no supported static ref validated; cited span or diff was absent"
    return "insufficient_evidence", "no explicit static evidence ref was available to validate"


def _validate_one_ref(
    evidence_ref: str,
    *,
    source_sql: str,
    candidate_sql: str,
    positive_sql: str | None,
) -> tuple[StaticEvidenceStatus, str]:
    if not evidence_ref.strip():
        return "rejected_invalid_ref", "empty evidence ref"
    prefix, sep, value = evidence_ref.partition(":")
    prefix = prefix.strip()
    value = value.strip()
    if sep != ":" or prefix not in SUPPORTED_STATIC_REF_PREFIXES or not value:
        return "rejected_invalid_ref", f"unsupported static evidence ref syntax: {evidence_ref!r}"
    if prefix in {"llm_rationale", "speedup", "timing", "taxonomy", "checker"}:
        return "rejected_invalid_ref", "disallowed non-static evidence ref"
    if prefix == "candidate_sql_span":
        return _check_literal_span("candidate_sql_span", value, candidate_sql)
    if prefix == "source_sql_span":
        return _check_literal_span("source_sql_span", value, source_sql)
    if prefix == "positive_sql_span":
        if positive_sql is None:
            return "rejected_missing_span", "positive SQL text is unavailable"
        return _check_literal_span("positive_sql_span", value, positive_sql)
    if prefix == "candidate_token_span":
        return _check_token_span(value, candidate_sql)
    if prefix == "source_candidate_diff":
        return _check_source_candidate_diff(value, source_sql=source_sql, candidate_sql=candidate_sql)
    return "rejected_invalid_ref", f"unsupported static evidence ref syntax: {evidence_ref!r}"


def _check_literal_span(label: str, needle: str, haystack: str) -> tuple[StaticEvidenceStatus, str]:
    if needle in haystack:
        return "validated_static_span", f"{label} literal substring exists"
    return "rejected_missing_span", f"{label} literal substring is absent"


def _check_token_span(needle: str, haystack: str) -> tuple[StaticEvidenceStatus, str]:
    normalized_needle = _normalize_tokens(needle)
    normalized_haystack = _normalize_tokens(haystack)
    if normalized_needle and normalized_needle in normalized_haystack:
        return "validated_static_span", "candidate_token_span normalized tokens exist"
    return "rejected_missing_span", "candidate_token_span normalized tokens are absent"


def _check_source_candidate_diff(
    marker: str,
    *,
    source_sql: str,
    candidate_sql: str,
) -> tuple[StaticEvidenceStatus, str]:
    normalized_source = _normalize_tokens(source_sql)
    normalized_candidate = _normalize_tokens(candidate_sql)
    if marker != "changed":
        return "rejected_invalid_ref", "source_candidate_diff currently supports only marker 'changed'"
    if normalized_source != normalized_candidate:
        return "validated_static_span", "source_candidate_diff:changed confirmed text differs"
    return "rejected_missing_span", "source and candidate SQL normalize to the same text"


def _normalize_tokens(sql: str) -> str:
    return " ".join(re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+|[<>=!]+|[(),.*+-/]", sql.lower()))
