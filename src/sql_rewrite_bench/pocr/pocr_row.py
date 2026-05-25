"""Row-level POCR draft model for future integration.

The object defined here is diagnostic scaffolding only. It does not aggregate
route-level POCR and must not be treated as an official paper metric output.
"""

from __future__ import annotations

from dataclasses import dataclass

from sql_rewrite_bench.pocr.evidence_validation import StageBValidationResult
from sql_rewrite_bench.pocr.models import SkillContract


@dataclass(frozen=True)
class POCRRowDraft:
    case_id: str
    pool: str
    engine: str
    method_id: str
    route_id: str
    denominator_eligible: bool
    curated_row_member: bool | None
    skill_present: bool
    annotation_present: bool
    stage_b_status: str
    validated_operation_atoms_count: int
    expected_operation_atoms_count: int
    validation_boundary: str
    fixture_only: bool = True
    official_metric: bool = False

    @classmethod
    def from_stage_b(
        cls,
        contract: SkillContract,
        stage_b: StageBValidationResult,
        *,
        denominator_eligible: bool,
        curated_row_member: bool | None = None,
        annotation_present: bool = True,
        validation_boundary: str = "fixture-only draft; not official POCR",
    ) -> "POCRRowDraft":
        return cls(
            case_id=stage_b.case_id or contract.case_id or "",
            pool=stage_b.pool or contract.pool or "",
            engine=stage_b.engine,
            method_id=stage_b.method_id,
            route_id=stage_b.route_id,
            denominator_eligible=denominator_eligible,
            curated_row_member=curated_row_member,
            skill_present=bool(contract.atoms),
            annotation_present=annotation_present,
            stage_b_status=stage_b.stage_b_status,
            validated_operation_atoms_count=stage_b.validated_operation_atoms_count,
            expected_operation_atoms_count=len(contract.operation_atoms),
            validation_boundary=validation_boundary,
        )

    def fixture_operation_ratio(self) -> float | None:
        """Return a fixture-only diagnostic ratio for tests, not route POCR."""

        if self.expected_operation_atoms_count == 0:
            return None
        return self.validated_operation_atoms_count / self.expected_operation_atoms_count
