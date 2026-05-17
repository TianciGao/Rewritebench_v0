# Evidence Ledger Validation Rules v1 Draft

Status: draft validation policy, not implementation-authorizing

Purpose: define validation rules for future ledger rows and synthetic fixtures before retained-evidence adapters or metrics computation are implemented.

This draft does not implement validators, adapters, metrics, report renderers, public runners, or reproduction CLI commands.

## Common Required Fields

Every ledger row must include:

- `record_id`
- `record_type`
- `case_set`
- `route`
- `method_role`
- `evidence_source`
- `status`
- `notes`

Every fixture row must also include:

- `fixture_only=true`
- `not_paper_evidence=true`
- `evidence_source=synthetic_fixture`

Case-scoped rows must include:

- `case_id`
- `pool`

Engine-scoped rows must include:

- `engine`

## Record-type Required Fields

`control_cell` requires `case_id`, `pool`, `case_set`, `engine`, `route`, `method_role=control`, `control_route`, `candidate_id`, `source_sql_path`, `candidate_sql_path`, `executed`, `exact`, `result_status`, `checker_status`, and `denominator_id` joined to `controls_360.csv`.

`rewrite_candidate_cell` requires `case_id`, `pool`, `case_set`, `denominator_id`, `engine`, `route=same_engine_rewrite`, `method_role`, `rewrite_method`, `candidate_id`, `source_sql_path`, `generated`, `ready`, `executed`, `exact`, `timed`, `result_status`, and `timing_eligible`.

`plan_observability_artifact` requires `case_set`, `route=plan_observability`, `method_role`, `artifact_id`, `plan_available`, `plan_artifact_path` when plan is available, `evidence_source`, and `retained_artifact_path` or fixture path.

`portability_candidate_cell` requires `case_id`, `pool=PORT`, `case_set`, `route=portability`, `method_role`, `candidate_id`, `source_engine`, `target_engine`, `candidate_sql_path`, `generated`, `ready`, `executed`, `exact`, `result_status`, and `checker_status`.

`verifier_support_pair` requires `case_set`, `route=verifier_support`, `method_role=verifier_support`, `support_pair_id`, `result_status`, `checker_status` or support status, `evidence_source`, and `retained_artifact_path` or fixture path.

`retained_summary_artifact` requires `case_set`, `route=summary`, `method_role=retained_legacy_reference`, `artifact_id`, `evidence_source`, `retained_artifact_path`, `metric_eligible=false`, and `notes`.

`user_run_candidate_cell` requires `case_id`, `pool`, `case_set`, `denominator_id` when benchmark-scoped, `engine`, `route`, `method_role=user_candidate`, `candidate_id`, `source_sql_path`, `candidate_sql_path`, `generated`, `ready`, `executed`, `exact`, `timed`, `result_status`, and non-case-local output paths.

## Record-type Forbidden Fields

`control_cell` must not populate `latency_ms` or `speedup_ratio` unless a future control timing policy explicitly authorizes it.

`plan_observability_artifact` must not populate `latency_ms`, `speedup_ratio`, `timed`, or `timing_eligible` as metric values.

`verifier_support_pair` must not populate `denominator_id`, `latency_ms`, `speedup_ratio`, or `timing_eligible`.

`retained_summary_artifact` must not set `metric_eligible=true` and must not carry candidate-level `exact`, `timed`, `latency_ms`, or `speedup_ratio` as canonical metric fields.

`portability_candidate_cell` must not use Track A same-engine denominator IDs unless a later portability denominator policy authorizes them.

## Allowed N.A. Statuses

Allowed explicit non-computable or missingness statuses:

- `unsupported`
- `not_applicable`
- `unknown`
- `verifier_unknown`
- `timing_missing`
- `target_timing_missing`
- `evidence_not_retained`
- `manual_review_required`
- `blocked`
- `N.A.`

These statuses must be represented in `status`, `result_status`, `na_reason`, `failure_stage`, `failure_type`, or `notes` as appropriate. They must not be silently dropped.

## Denominator ID Validation Rules

- `rewrite_candidate_cell` same-engine rows require a `denominator_id` that joins to `case_sets/common_core_v0/denominator_same_engine_120.csv`.
- `user_run_candidate_cell` benchmark-scoped rows require the same Track A denominator join.
- `control_cell` rows require a `denominator_id` that joins to `case_sets/common_core_v0/controls_360.csv`.
- `plan_observability_artifact`, `verifier_support_pair`, and `retained_summary_artifact` rows should leave `denominator_id` blank unless a future policy explicitly defines a denominator-aware support metric.
- `portability_candidate_cell` rows use separate portability semantics and should not use Track A denominator IDs by default.

## Status Consistency Rules

- `latency_ms` and `speedup_ratio` require `timed=true` and `timing_eligible=true`.
- `timing_missing` requires `timed=false` or `timing_eligible=false`.
- `target_timing_missing` requires `record_type=portability_candidate_cell`.
- `verifier_unknown` should appear only on verifier support or semantic-equivalence support rows.
- `mismatch` should require `executed=true` and `exact=false`.
- `checker_rejected` on a hard-negative `control_cell` may be valid when `checker_status=reject_expected`.
- `N.A.` requires `na_reason`.

## No-global-leaderboard Guard

Validation must fail any aggregate or fixture that collapses incompatible `record_type`, `route`, `method_role`, `engine`, or denominator families into a single leaderboard row.

## No-metric-computation Guard

Fixture and adapter validation outputs must not include computed metric aggregates such as Generation Rate, Execution Coverage Rate, Result Consistency Rate, Semantic Equivalence Rate, GM_Speedup, Speedup Ratio Percentiles, Attribution Coverage, Cross-Engine Execution, Cross-Engine Consistency, Speedup Retention, or Regression@20.

## No-case-local-runs-output Guard

Future materialized ledgers and public runner outputs must not write into case-local `runs/`. Synthetic fixtures may use fixture-local paths under the audit directory.

## Public Hygiene Expectations

Future materialized ledgers must not expose:

- absolute local paths;
- raw stdout/stderr paths;
- WSL or host-specific traces;
- localhost or private endpoints;
- API keys or tokens;
- prompt/model traces;
- unsanitized raw logs.

## Failure Behavior

Future validators should fail closed for missing identity fields, denominator-join mismatches, forbidden field population, unsafe paths, and metric aggregates. They may warn for nullable support fields only when `status`, `na_reason`, or `notes` explains the missingness.
