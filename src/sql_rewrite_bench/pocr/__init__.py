"""Parse-only POCR skills.md contract helpers."""

from sql_rewrite_bench.pocr.annotation_client import (
    AnnotationCallResult,
    AnnotationClientConfig,
    FakeAnnotationClient,
    build_annotation_client,
)
from sql_rewrite_bench.pocr.annotation_schema import (
    ANNOTATION_SCHEMA_VERSION,
    AtomJudgment,
    CandidateAnnotation,
    annotation_from_mapping,
    annotation_to_json_dict,
    validate_candidate_annotation,
)
from sql_rewrite_bench.pocr.evidence_validation import (
    AtomEvidenceValidation,
    StageBValidationResult,
    SyntheticEvidenceRef,
    validate_stage_b,
)
from sql_rewrite_bench.pocr.inventory import (
    CommonCoreSkillInventory,
    build_common_core_inventory,
    write_parse_only_report,
)
from sql_rewrite_bench.pocr.models import (
    SkillAtom,
    SkillContract,
    SkillParseResult,
    SkillValidationIssue,
)
from sql_rewrite_bench.pocr.pocr_row import POCRRowDraft
from sql_rewrite_bench.pocr.prompt_builder import AnnotationPromptInputs, build_annotation_prompt
from sql_rewrite_bench.pocr.skills_parser import parse_skills_file, parse_skills_text
from sql_rewrite_bench.pocr.validation import validate_skill_contract

__all__ = [
    "ANNOTATION_SCHEMA_VERSION",
    "AnnotationCallResult",
    "AnnotationClientConfig",
    "AnnotationPromptInputs",
    "AtomEvidenceValidation",
    "AtomJudgment",
    "CandidateAnnotation",
    "CommonCoreSkillInventory",
    "FakeAnnotationClient",
    "POCRRowDraft",
    "SkillAtom",
    "SkillContract",
    "SkillParseResult",
    "SkillValidationIssue",
    "StageBValidationResult",
    "SyntheticEvidenceRef",
    "annotation_from_mapping",
    "annotation_to_json_dict",
    "build_annotation_client",
    "build_annotation_prompt",
    "build_common_core_inventory",
    "parse_skills_file",
    "parse_skills_text",
    "validate_candidate_annotation",
    "validate_stage_b",
    "validate_skill_contract",
    "write_parse_only_report",
]
