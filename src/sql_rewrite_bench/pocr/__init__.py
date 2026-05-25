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
from sql_rewrite_bench.pocr.annotation_resolver import (
    ResolvedAnnotationArtifact,
    annotation_artifact_inventory_fields,
    annotation_artifacts_to_csv_rows,
    resolve_annotation_artifacts,
    write_annotation_artifact_inventory,
)
from sql_rewrite_bench.pocr.candidate_resolver import (
    CandidateSource,
    candidate_inventory_fields,
    candidate_sources_to_csv_rows,
    resolve_candidate_sources,
)
from sql_rewrite_bench.pocr.draft_runner import (
    DiagnosticPOCRDraftRow,
    build_diagnostic_drafts,
    diagnostic_draft_fields,
    diagnostic_draft_to_csv_rows,
    write_diagnostic_draft_csv,
)
from sql_rewrite_bench.pocr.diagnostic_output_schema import (
    POCRDiagnosticPoolSummary,
    POCRDiagnosticRow,
    diagnostic_row_fields,
    diagnostic_rows_to_csv_rows,
    diagnostic_summaries_to_csv_rows,
    diagnostic_summary_fields,
    render_diagnostic_markdown_report,
    summarize_by_pool,
    write_diagnostic_rows_csv,
    write_diagnostic_summary_csv,
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
from sql_rewrite_bench.pocr.json_output_guard import GuardedJsonResult, guarded_json_loads
from sql_rewrite_bench.pocr.pocr_row import POCRRowDraft
from sql_rewrite_bench.pocr.prompt_builder import AnnotationPromptInputs, build_annotation_prompt
from sql_rewrite_bench.pocr.skills_parser import parse_skills_file, parse_skills_text
from sql_rewrite_bench.pocr.stage_b_static_runner import (
    StaticStageBDiagnosticRow,
    build_static_stage_b_diagnostic_rows,
    static_stage_b_diagnostic_fields,
    static_stage_b_diagnostic_to_csv_rows,
    write_static_stage_b_diagnostic_csv,
)
from sql_rewrite_bench.pocr.static_evidence import (
    StaticAtomEvidenceValidation,
    StaticStageBValidationResult,
    validate_static_stage_b,
)
from sql_rewrite_bench.pocr.user_facade import (
    POCRDiagnosticFacadeResult,
    run_pocr_diagnostic_user_facade,
)
from sql_rewrite_bench.pocr.user_output_adapter import (
    POCRDiagnosticOutputPaths,
    write_pocr_diagnostic_user_outputs,
)
from sql_rewrite_bench.pocr.validation import validate_skill_contract

__all__ = [
    "ANNOTATION_SCHEMA_VERSION",
    "AnnotationCallResult",
    "AnnotationClientConfig",
    "AnnotationPromptInputs",
    "AtomEvidenceValidation",
    "AtomJudgment",
    "CandidateSource",
    "CandidateAnnotation",
    "CommonCoreSkillInventory",
    "DiagnosticPOCRDraftRow",
    "FakeAnnotationClient",
    "GuardedJsonResult",
    "POCRDiagnosticFacadeResult",
    "POCRDiagnosticOutputPaths",
    "POCRDiagnosticPoolSummary",
    "POCRDiagnosticRow",
    "POCRRowDraft",
    "ResolvedAnnotationArtifact",
    "SkillAtom",
    "SkillContract",
    "SkillParseResult",
    "SkillValidationIssue",
    "StageBValidationResult",
    "StaticAtomEvidenceValidation",
    "StaticStageBDiagnosticRow",
    "StaticStageBValidationResult",
    "SyntheticEvidenceRef",
    "annotation_artifact_inventory_fields",
    "annotation_artifacts_to_csv_rows",
    "annotation_from_mapping",
    "annotation_to_json_dict",
    "build_diagnostic_drafts",
    "build_annotation_client",
    "build_annotation_prompt",
    "build_common_core_inventory",
    "build_static_stage_b_diagnostic_rows",
    "candidate_inventory_fields",
    "candidate_sources_to_csv_rows",
    "diagnostic_draft_fields",
    "diagnostic_draft_to_csv_rows",
    "diagnostic_row_fields",
    "diagnostic_rows_to_csv_rows",
    "diagnostic_summaries_to_csv_rows",
    "diagnostic_summary_fields",
    "guarded_json_loads",
    "parse_skills_file",
    "parse_skills_text",
    "render_diagnostic_markdown_report",
    "resolve_annotation_artifacts",
    "resolve_candidate_sources",
    "run_pocr_diagnostic_user_facade",
    "summarize_by_pool",
    "static_stage_b_diagnostic_fields",
    "static_stage_b_diagnostic_to_csv_rows",
    "validate_candidate_annotation",
    "validate_static_stage_b",
    "validate_stage_b",
    "validate_skill_contract",
    "write_annotation_artifact_inventory",
    "write_diagnostic_draft_csv",
    "write_diagnostic_rows_csv",
    "write_diagnostic_summary_csv",
    "write_pocr_diagnostic_user_outputs",
    "write_static_stage_b_diagnostic_csv",
    "write_parse_only_report",
]
