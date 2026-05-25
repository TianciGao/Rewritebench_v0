"""Transformation-aware POCR Stage B operation evidence policy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from sql_rewrite_bench.pocr.annotation_schema import CandidateAnnotation, validate_candidate_annotation
from sql_rewrite_bench.pocr.models import AtomCategory, SkillContract, SkillValidationIssue
from sql_rewrite_bench.pocr.transformation_evidence import (
    candidate_aligns_with_positive_span,
    is_source_like_noop,
    normalize_sql_for_pocr_diff,
    source_candidate_changed,
    span_present_in_candidate_but_absent_or_different_from_source,
)

TransformationEvidenceStatus = Literal[
    "presence_only",
    "transformation_supported",
    "insufficient_transformation_evidence",
    "rejected_noop_equivalent",
    "schema_invalid",
    "atom_not_in_contract",
    "invalid_ref",
    "validated_static_span",
    "rejected_missing_span",
]

SUPPORTED_TRANSFORMATION_REF_PREFIXES = {
    "candidate_sql_span",
    "source_sql_span",
    "positive_sql_span",
    "candidate_token_span",
    "source_candidate_diff",
}


@dataclass(frozen=True)
class TransformationAtomEvidenceValidation:
    atom_id: str
    atom_type: AtomCategory | str
    observed_status: str
    evidence_status: TransformationEvidenceStatus
    evidence_refs: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class TransformationStageBValidationResult:
    case_id: str | None
    pool: str | None
    engine: str
    method_id: str
    route_id: str
    schema_valid: bool
    source_like_noop: bool
    issues: tuple[SkillValidationIssue, ...]
    atom_results: tuple[TransformationAtomEvidenceValidation, ...]

    @property
    def stage_b_status(self) -> str:
        if not self.schema_valid:
            return "schema_invalid"
        if self.transformation_supported_operation_atoms_count:
            return "transformation_evidence_partial"
        if self.rejected_noop_equivalent_operation_atoms_count:
            return "rejected_noop_equivalent"
        if self.presence_only_operation_atoms_count:
            return "presence_only"
        if any(atom.evidence_status in {"invalid_ref", "rejected_missing_span"} for atom in self.atom_results):
            return "transformation_evidence_rejected"
        return "insufficient_transformation_evidence"

    @property
    def presence_only_operation_atoms_count(self) -> int:
        return _operation_status_count(self.atom_results, "presence_only")

    @property
    def transformation_supported_operation_atoms_count(self) -> int:
        return _operation_status_count(self.atom_results, "transformation_supported")

    @property
    def insufficient_transformation_evidence_operation_atoms_count(self) -> int:
        return _operation_status_count(self.atom_results, "insufficient_transformation_evidence")

    @property
    def rejected_noop_equivalent_operation_atoms_count(self) -> int:
        return _operation_status_count(self.atom_results, "rejected_noop_equivalent")

    @property
    def schema_invalid_atoms_count(self) -> int:
        return _operation_status_count(self.atom_results, "schema_invalid")


def validate_transformation_stage_b(
    contract: SkillContract,
    annotation: CandidateAnnotation,
    *,
    source_sql: str,
    candidate_sql: str,
    positive_sql: str | None = None,
    negative_sql: str | None = None,
) -> TransformationStageBValidationResult:
    """Validate Stage A evidence refs with transformation-aware operation rules."""

    del negative_sql
    issues = validate_candidate_annotation(annotation, contract)
    schema_valid = not any(issue.severity == "error" for issue in issues)
    contract_atom_ids = {atom.atom_id for atom in contract.atoms}
    source_like = is_source_like_noop(source_sql, candidate_sql)
    atom_results: list[TransformationAtomEvidenceValidation] = []

    for atom in annotation.atoms:
        if atom.atom_id not in contract_atom_ids:
            atom_results.append(
                TransformationAtomEvidenceValidation(
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
                TransformationAtomEvidenceValidation(
                    atom_id=atom.atom_id,
                    atom_type=atom.atom_type,
                    observed_status=atom.observed_status,
                    evidence_status="schema_invalid",
                    evidence_refs=atom.evidence_refs,
                    reason="annotation schema validation failed",
                )
            )
            continue
        if atom.atom_type == "operation_atom":
            status, reason = _validate_operation_refs(
                atom.evidence_refs,
                observed_status=atom.observed_status,
                source_sql=source_sql,
                candidate_sql=candidate_sql,
                positive_sql=positive_sql,
                source_like_noop=source_like,
            )
        else:
            status, reason = _validate_semantic_guard_refs(
                atom.evidence_refs,
                source_sql=source_sql,
                candidate_sql=candidate_sql,
                positive_sql=positive_sql,
            )
        atom_results.append(
            TransformationAtomEvidenceValidation(
                atom_id=atom.atom_id,
                atom_type=atom.atom_type,
                observed_status=atom.observed_status,
                evidence_status=status,
                evidence_refs=atom.evidence_refs,
                reason=reason,
            )
        )

    return TransformationStageBValidationResult(
        case_id=annotation.case_id,
        pool=annotation.pool,
        engine=annotation.engine,
        method_id=annotation.method_id,
        route_id=annotation.route_id,
        schema_valid=schema_valid,
        source_like_noop=source_like,
        issues=issues,
        atom_results=tuple(atom_results),
    )


def _validate_operation_refs(
    evidence_refs: tuple[str, ...],
    *,
    observed_status: str,
    source_sql: str,
    candidate_sql: str,
    positive_sql: str | None,
    source_like_noop: bool,
) -> tuple[TransformationEvidenceStatus, str]:
    if observed_status != "implemented":
        return "insufficient_transformation_evidence", "Stage A did not mark the operation atom implemented"
    if not evidence_refs:
        if source_like_noop:
            return "rejected_noop_equivalent", "candidate normalizes as source-like/no-op and no transformation ref was provided"
        return "insufficient_transformation_evidence", "no explicit transformation evidence refs were provided"

    parsed = [_parse_ref(ref) for ref in evidence_refs]
    invalid = [reason for prefix, value, reason in parsed if prefix is None]
    if invalid:
        return "invalid_ref", invalid[0]

    candidate_spans = [value for prefix, value, _ in parsed if prefix == "candidate_sql_span"]
    source_spans = [value for prefix, value, _ in parsed if prefix == "source_sql_span"]
    positive_spans = [value for prefix, value, _ in parsed if prefix == "positive_sql_span"]
    candidate_token_spans = [value for prefix, value, _ in parsed if prefix == "candidate_token_span"]
    diff_markers = [value for prefix, value, _ in parsed if prefix == "source_candidate_diff"]

    diff_changed = any(marker == "changed" and source_candidate_changed(source_sql, candidate_sql) for marker in diff_markers)
    diff_invalid = any(marker != "changed" for marker in diff_markers)
    if diff_invalid:
        return "invalid_ref", "source_candidate_diff currently supports only marker 'changed'"

    candidate_specific = any(
        span_present_in_candidate_but_absent_or_different_from_source(
            span,
            source_sql=source_sql,
            candidate_sql=candidate_sql,
        )
        for span in candidate_spans
    )
    token_specific = any(
        _token_span_present_in_candidate_but_absent_from_source(
            span,
            source_sql=source_sql,
            candidate_sql=candidate_sql,
        )
        for span in candidate_token_spans
    )
    positive_aligned_specific = any(
        candidate_aligns_with_positive_span(span, candidate_sql=candidate_sql, positive_sql=positive_sql)
        and span_present_in_candidate_but_absent_or_different_from_source(
            span,
            source_sql=source_sql,
            candidate_sql=candidate_sql,
        )
        for span in [*candidate_spans, *positive_spans]
    )
    span_present = any(_span_present(span, candidate_sql) for span in candidate_spans) or any(
        _span_present(span, source_sql) for span in source_spans
    ) or any(_span_present(span, positive_sql or "") for span in positive_spans) or any(
        _token_span_present(span, candidate_sql) for span in candidate_token_spans
    )

    if source_like_noop:
        if span_present:
            return "presence_only", "candidate is source-like/no-op; cited span proves presence only"
        return "rejected_noop_equivalent", "candidate normalizes as source-like/no-op"
    if diff_changed and (candidate_specific or token_specific or positive_aligned_specific):
        return "transformation_supported", "candidate-specific or positive-aligned span is paired with source_candidate_diff:changed"
    if diff_changed:
        return "insufficient_transformation_evidence", "source_candidate_diff:changed is not atom-specific without a candidate/positive span"
    if span_present:
        return "presence_only", "cited span exists but does not establish a transformation relative to source"
    if candidate_specific or token_specific or positive_aligned_specific:
        return "presence_only", "candidate-specific span lacks source_candidate_diff:changed"
    return "insufficient_transformation_evidence", "no cited span or diff established transformation support"


def _validate_semantic_guard_refs(
    evidence_refs: tuple[str, ...],
    *,
    source_sql: str,
    candidate_sql: str,
    positive_sql: str | None,
) -> tuple[TransformationEvidenceStatus, str]:
    if not evidence_refs:
        return "insufficient_transformation_evidence", "no semantic guard evidence refs were provided"
    for ref in evidence_refs:
        prefix, value, reason = _parse_ref(ref)
        if prefix is None:
            return "invalid_ref", reason
        if prefix == "candidate_sql_span" and _span_present(value, candidate_sql):
            return "validated_static_span", "semantic guard candidate_sql_span exists"
        if prefix == "source_sql_span" and _span_present(value, source_sql):
            return "validated_static_span", "semantic guard source_sql_span exists"
        if prefix == "positive_sql_span" and positive_sql is not None and _span_present(value, positive_sql):
            return "validated_static_span", "semantic guard positive_sql_span exists"
        if prefix == "candidate_token_span" and _token_span_present(value, candidate_sql):
            return "validated_static_span", "semantic guard candidate_token_span exists"
        if prefix == "source_candidate_diff" and value == "changed" and source_candidate_changed(source_sql, candidate_sql):
            return "validated_static_span", "semantic guard source_candidate_diff:changed confirmed"
    return "rejected_missing_span", "semantic guard refs were syntactically valid but not present"


def _parse_ref(evidence_ref: str) -> tuple[str | None, str, str]:
    if not evidence_ref.strip():
        return None, "", "empty evidence ref"
    prefix, sep, value = evidence_ref.partition(":")
    prefix = prefix.strip()
    value = value.strip()
    if sep != ":" or prefix not in SUPPORTED_TRANSFORMATION_REF_PREFIXES or not value:
        return None, value, f"unsupported transformation evidence ref syntax: {evidence_ref!r}"
    return prefix, value, ""


def _span_present(span: str, sql: str) -> bool:
    return bool(normalize_sql_for_pocr_diff(span)) and normalize_sql_for_pocr_diff(span) in normalize_sql_for_pocr_diff(sql)


def _token_span_present(span: str, sql: str) -> bool:
    return _span_present(span, sql)


def _token_span_present_in_candidate_but_absent_from_source(
    span: str,
    *,
    source_sql: str,
    candidate_sql: str,
) -> bool:
    normalized_span = normalize_sql_for_pocr_diff(span)
    return bool(normalized_span) and normalized_span in normalize_sql_for_pocr_diff(candidate_sql) and normalized_span not in normalize_sql_for_pocr_diff(source_sql)


def _operation_status_count(
    atom_results: tuple[TransformationAtomEvidenceValidation, ...],
    status: str,
) -> int:
    return sum(
        1
        for atom in atom_results
        if atom.atom_type == "operation_atom" and atom.evidence_status == status
    )
