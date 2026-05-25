"""Stage B evidence-validation interface for POCR annotations.

Stage B is fail-closed in this scaffold. LLM rationale is not independent
evidence, speedup is not evidence, taxonomy tags are not operation evidence,
and this module does not compute official POCR.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from sql_rewrite_bench.pocr.annotation_schema import CandidateAnnotation, validate_candidate_annotation
from sql_rewrite_bench.pocr.models import AtomCategory, SkillContract, SkillValidationIssue

EvidenceStatus = Literal["validated", "rejected", "insufficient_evidence", "schema_invalid", "atom_not_in_contract"]


@dataclass(frozen=True)
class SyntheticEvidenceRef:
    """Fixture-only independent evidence reference used by offline tests."""

    evidence_id: str
    atom_id: str
    allowed_statuses: tuple[str, ...] = ("implemented",)
    evidence_kind: str = "synthetic_fixture"


@dataclass(frozen=True)
class AtomEvidenceValidation:
    atom_id: str
    atom_type: AtomCategory | str
    observed_status: str
    evidence_status: EvidenceStatus
    evidence_refs: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class StageBValidationResult:
    case_id: str | None
    pool: str | None
    engine: str
    method_id: str
    route_id: str
    schema_valid: bool
    issues: tuple[SkillValidationIssue, ...]
    atom_results: tuple[AtomEvidenceValidation, ...]

    @property
    def stage_b_status(self) -> str:
        if not self.schema_valid:
            return "schema_invalid"
        if any(atom.evidence_status == "validated" for atom in self.atom_results):
            return "partial_validated"
        return "insufficient_evidence"

    @property
    def validated_operation_atoms_count(self) -> int:
        return sum(
            1
            for atom in self.atom_results
            if atom.atom_type == "operation_atom" and atom.evidence_status == "validated"
        )


def validate_stage_b(
    contract: SkillContract,
    annotation: CandidateAnnotation,
    *,
    candidate_sql: str | None = None,
    candidate_path: str | None = None,
    synthetic_evidence_refs: tuple[SyntheticEvidenceRef, ...] = (),
) -> StageBValidationResult:
    """Validate annotation schema and fixture-only independent evidence refs."""

    issues = validate_candidate_annotation(annotation, contract)
    if candidate_path and annotation.candidate_path and candidate_path != annotation.candidate_path:
        issues = issues + (
            _issue(contract, "candidate_path_mismatch", f"{annotation.candidate_path} != {candidate_path}"),
        )
    if candidate_sql is not None and not candidate_sql.strip():
        issues = issues + (_issue(contract, "empty_candidate_sql", "candidate SQL text is empty"),)

    schema_valid = not any(issue.severity == "error" for issue in issues)
    contract_atom_ids = {atom.atom_id for atom in contract.atoms}
    evidence_by_id = {ref.evidence_id: ref for ref in synthetic_evidence_refs}
    atom_results: list[AtomEvidenceValidation] = []

    for atom in annotation.atoms:
        if atom.atom_id not in contract_atom_ids:
            atom_results.append(
                AtomEvidenceValidation(
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
                AtomEvidenceValidation(
                    atom_id=atom.atom_id,
                    atom_type=atom.atom_type,
                    observed_status=atom.observed_status,
                    evidence_status="schema_invalid",
                    evidence_refs=atom.evidence_refs,
                    reason="annotation schema validation failed",
                )
            )
            continue
        status, reason = _validate_atom_evidence(atom.atom_id, atom.observed_status, atom.evidence_refs, evidence_by_id)
        atom_results.append(
            AtomEvidenceValidation(
                atom_id=atom.atom_id,
                atom_type=atom.atom_type,
                observed_status=atom.observed_status,
                evidence_status=status,
                evidence_refs=atom.evidence_refs,
                reason=reason,
            )
        )

    return StageBValidationResult(
        case_id=annotation.case_id,
        pool=annotation.pool,
        engine=annotation.engine,
        method_id=annotation.method_id,
        route_id=annotation.route_id,
        schema_valid=schema_valid,
        issues=issues,
        atom_results=tuple(atom_results),
    )


def _validate_atom_evidence(
    atom_id: str,
    observed_status: str,
    evidence_refs: tuple[str, ...],
    evidence_by_id: dict[str, SyntheticEvidenceRef],
) -> tuple[EvidenceStatus, str]:
    if not evidence_refs:
        return "insufficient_evidence", "no independent evidence refs were provided"

    for evidence_ref in evidence_refs:
        if evidence_ref.startswith("llm_rationale:"):
            return "rejected", "LLM rationale is not independent evidence"
        if evidence_ref.startswith("speedup:") or evidence_ref.startswith("timing:"):
            return "rejected", "speedup or timing is not POCR atom evidence"
        if evidence_ref.startswith("taxonomy:"):
            return "rejected", "taxonomy tags are not operation evidence"
        evidence = evidence_by_id.get(evidence_ref)
        if evidence is None:
            return "insufficient_evidence", f"evidence ref {evidence_ref!r} is not available to Stage B"
        if evidence.atom_id != atom_id:
            return "rejected", f"evidence ref {evidence_ref!r} belongs to atom {evidence.atom_id!r}"
        if observed_status not in evidence.allowed_statuses:
            return "rejected", f"evidence ref {evidence_ref!r} does not support status {observed_status!r}"

    return "validated", "all fixture evidence refs match the atom and observed status"


def _issue(contract: SkillContract, code: str, message: str) -> SkillValidationIssue:
    return SkillValidationIssue(
        case_id=contract.case_id,
        pool=contract.pool,
        skills_path=contract.skills_path,
        code=code,
        message=message,
    )
