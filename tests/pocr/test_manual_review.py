from sql_rewrite_bench.pocr.evidence_ref_linter import EvidenceRefLintRow
from sql_rewrite_bench.pocr.manual_review import (
    dedupe_manual_review_rows,
    manual_review_rows_to_csv_rows,
    review_rows_for_lint,
    review_rows_for_retry_plan,
    review_rows_for_stage_b,
)
from sql_rewrite_bench.pocr.operation_evidence_policy import (
    TransformationAtomEvidenceValidation,
    TransformationStageBValidationResult,
)
from sql_rewrite_bench.pocr.retry_planner import RetryPlanRow


def _stage_b_result() -> TransformationStageBValidationResult:
    return TransformationStageBValidationResult(
        case_id="PERF_0006",
        pool="PERF",
        engine="postgres",
        method_id="direct_llm_repair_1",
        route_id="direct_llm_repair_1_pg40_pocr_diagnostic",
        schema_valid=True,
        source_like_noop=False,
        issues=(),
        atom_results=(
            TransformationAtomEvidenceValidation(
                atom_id="A1",
                atom_type="operation_atom",
                observed_status="implemented",
                evidence_status="transformation_supported",
                evidence_refs=("candidate_sql_span:JOIN x", "source_candidate_diff:changed"),
                reason="accepted",
            ),
            TransformationAtomEvidenceValidation(
                atom_id="A2",
                atom_type="operation_atom",
                observed_status="implemented",
                evidence_status="presence_only",
                evidence_refs=("candidate_sql_span:WHERE x = 1", "source_candidate_diff:changed"),
                reason="presence only",
            ),
        ),
    )


def test_manual_review_rows_for_stage_b_supported_and_under_accept() -> None:
    rows = review_rows_for_stage_b(_stage_b_result())

    reasons = {row.review_reason for row in rows}
    assert reasons == {"transformation_supported_atom", "possible_under_accept"}
    assert all(row.diagnostic_only for row in rows)
    assert all(row.official_pocr_computed is False for row in rows)
    assert manual_review_rows_to_csv_rows(rows)[0]["official_pocr_computed"] == "false"


def test_manual_review_rows_for_retry_plan() -> None:
    rows = review_rows_for_retry_plan(
        [
            RetryPlanRow(
                case_id="PERF_0017",
                pool="PERF",
                engine="postgres",
                method_id="direct_llm_repair_1",
                route_id="direct_llm_repair_1_pg40_pocr_diagnostic",
                candidate_sha256="abc",
                current_status="timeout",
                retry_eligible=True,
                retry_reason="timeout",
                retry_requires_explicit_flag=True,
                prior_attempt_count=1,
                recommendation="retry",
            )
        ]
    )

    assert rows[0].review_reason == "timeout"
    assert rows[0].suggested_review_action == "retry_annotation"


def test_manual_review_rows_for_lint_and_dedupe() -> None:
    lint = EvidenceRefLintRow(
        case_id="PERF_0006",
        pool="PERF",
        atom_id="A1",
        atom_type="operation_atom",
        observed_status="implemented",
        evidence_ref="candidate_sql_span:WHERE x = 1",
        lint_status="issue",
        issue_type="candidate_sql_span_only",
        severity="warning",
        recommendation="add diff",
    )

    rows = review_rows_for_lint(
        [lint, lint],
        engine="postgres",
        method_id="direct_llm_repair_1",
        route_id="direct_llm_repair_1_pg40_pocr_diagnostic",
    )

    assert len(dedupe_manual_review_rows(rows)) == 1
    assert rows[0].suggested_review_action == "inspect_candidate_source_diff"
