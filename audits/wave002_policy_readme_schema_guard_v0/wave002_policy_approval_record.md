# Wave 002 Policy Approval Record

## Purpose

This record answers the wave 002 policy questions in batch so the next case-package generation wave can proceed without per-case manual intervention where the approved guardrails apply.

## Approved Low-risk Policies

1. Static-inferred hard-negative reason may be used for package creation only if marked `needs_review` and not treated as paper-facing approval.
2. Validation scripts may be retained as legacy assets with a standard output-policy caveat.
3. Spark, local-path, and raw plan artifacts must be sanitized or archive-mapped; raw local-path artifacts must not be copied.
4. Missing retained evidence may be represented as `evidence_not_retained` if source/positive/checker/package core assets are otherwise complete.
5. Validation script execution is not required for package creation; scripts are retained assets only unless explicitly run later.
6. `package_validation_summary.json` must follow the schema guard and must not include task/global repository fields.
7. Case README files must follow public template v1.
8. No case can enter `case_sets/` or denominators in wave 002.
9. Raw logs, prompt/token/API traces, stdout/stderr/debug payloads, and local-path artifacts remain forbidden public package contents.

## Scope Of Approval

This approval applies only to wave 002 candidate selection and future package generation under the stated boundaries. It does not authorize case migration in this task, official staged/backlog membership, denominator changes, reports/results updates, metric computation, paper table rendering, raw legacy evidence changes, DB validation, timing runs, or LLM calls.

## Result

The 28 wave 001 deferred cases can be treated as `wave_002_policy_approved_candidate` for a separately authorized wave 002 package generation task, subject to fail-closed validation and skip dossiers for any case that violates the policy conditions.
