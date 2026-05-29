"""Data models for parse-only POCR skills.md contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

AtomCategory = Literal["operation_atom", "semantic_guard_atom", "unknown"]
IssueSeverity = Literal["error", "warning"]


@dataclass(frozen=True)
class SkillAtom:
    """One row from the Atom Protocol table.

    The parser preserves both normalized fields and the original table mapping.
    It does not infer operation semantics from SQL, taxonomy, or candidate text.
    """

    atom_id: str
    category: AtomCategory
    atom_type: str
    risk: str
    weight_raw: str
    weight: float | None
    requirement: str
    source_row_number: int | None = None
    raw_fields: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SkillContract:
    """Parsed root-level case-local skills.md contract."""

    skills_path: Path | None
    case_id: str | None
    pool: str | None
    atoms: tuple[SkillAtom, ...]
    has_atom_protocol: bool
    has_required_candidate_annotation_shape: bool
    has_review_boundaries: bool
    raw_text: str

    @property
    def operation_atoms(self) -> tuple[SkillAtom, ...]:
        return tuple(atom for atom in self.atoms if atom.category == "operation_atom")

    @property
    def semantic_guard_atoms(self) -> tuple[SkillAtom, ...]:
        return tuple(atom for atom in self.atoms if atom.category == "semantic_guard_atom")


@dataclass(frozen=True)
class SkillValidationIssue:
    """A non-mutating parser/contract validation finding."""

    case_id: str | None
    pool: str | None
    skills_path: Path | None
    code: str
    message: str
    severity: IssueSeverity = "error"


@dataclass(frozen=True)
class SkillParseResult:
    """Parse result plus validation issues."""

    contract: SkillContract | None
    issues: tuple[SkillValidationIssue, ...]

    @property
    def ok(self) -> bool:
        return self.contract is not None and not any(issue.severity == "error" for issue in self.issues)
