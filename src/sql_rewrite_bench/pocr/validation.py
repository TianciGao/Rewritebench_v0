"""Validation helpers for parse-only skills.md contracts."""

from __future__ import annotations

from collections.abc import Iterable

from sql_rewrite_bench.pocr.models import SkillContract, SkillValidationIssue


def validate_skill_contract(
    contract: SkillContract,
    *,
    expected_case_id: str | None = None,
    expected_pool: str | None = None,
) -> Iterable[SkillValidationIssue]:
    """Yield non-mutating validation issues for one parsed contract."""

    if not contract.case_id:
        yield _issue(contract, "missing_case_id", "skills.md does not declare a case_id")
    if not contract.pool:
        yield _issue(contract, "missing_pool", "skills.md does not declare a pool")

    if expected_case_id is not None and contract.case_id != expected_case_id:
        yield _issue(
            contract,
            "case_id_mismatch",
            f"parsed case_id {contract.case_id!r} does not match expected {expected_case_id!r}",
        )
    if expected_pool is not None and contract.pool != expected_pool:
        yield _issue(
            contract,
            "pool_mismatch",
            f"parsed pool {contract.pool!r} does not match expected {expected_pool!r}",
        )

    if not contract.has_atom_protocol:
        yield _issue(contract, "missing_atom_protocol", "skills.md is missing the Atom Protocol section")
    if not contract.atoms:
        yield _issue(contract, "missing_atom_table", "Atom Protocol table was not parsed")
    if not contract.operation_atoms:
        yield _issue(contract, "missing_operation_atom", "Atom Protocol has no operation_atom rows")
    if not contract.semantic_guard_atoms:
        yield _issue(contract, "missing_semantic_guard_atom", "Atom Protocol has no semantic_guard_atom rows")
    if not contract.has_required_candidate_annotation_shape:
        yield _issue(
            contract,
            "missing_required_candidate_annotation_shape",
            "skills.md is missing Required Candidate Annotation Shape",
        )
    if not contract.has_review_boundaries:
        yield _issue(contract, "missing_review_boundaries", "skills.md is missing Review Boundaries")

    for atom in contract.atoms:
        if not atom.atom_id:
            yield _issue(contract, "missing_atom_id", "Atom Protocol row is missing atom id")
        if atom.category == "unknown":
            yield _issue(
                contract,
                "unknown_atom_category",
                f"Atom {atom.atom_id!r} has unsupported category {atom.raw_fields.get('category')!r}",
            )
        if not atom.atom_type:
            yield _issue(contract, "missing_atom_type", f"Atom {atom.atom_id!r} is missing type")
        if not atom.requirement:
            yield _issue(contract, "missing_atom_requirement", f"Atom {atom.atom_id!r} is missing requirement")
        if atom.weight_raw and atom.weight is None:
            yield _issue(contract, "invalid_atom_weight", f"Atom {atom.atom_id!r} has invalid weight {atom.weight_raw!r}")


def _issue(contract: SkillContract, code: str, message: str) -> SkillValidationIssue:
    return SkillValidationIssue(
        case_id=contract.case_id,
        pool=contract.pool,
        skills_path=contract.skills_path,
        code=code,
        message=message,
    )
