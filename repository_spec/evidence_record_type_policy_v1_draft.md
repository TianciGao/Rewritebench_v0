# Evidence Record Type Policy v1 Draft

Status: draft policy, not implementation-authorizing

Purpose: define evidence ledger record types, required fields, forbidden fields, and metric eligibility boundaries.

## Record Type Values

Allowed draft values:

- `control_cell`
- `rewrite_candidate_cell`
- `plan_observability_artifact`
- `portability_candidate_cell`
- `verifier_support_pair`
- `retained_summary_artifact`
- `user_run_candidate_cell`

## `control_cell`

Represents: `case x engine x control_route`.

Required fields: `case_id`, `pool`, `case_set`, `engine`, `route`, `method_role=control`, `candidate_id`, `source_sql_path`, `candidate_sql_path`, `executed`, `exact`, `result_status`, `checker_status`, `evidence_source`, `retained_artifact_path`, `notes`.

Forbidden or discouraged fields: `speedup` should be null; `latency_ms` should be null unless the control timing policy is later approved.

Metric eligibility: eligible for control/checker quality summaries, source-positive equivalence evidence, and hard-negative rejection evidence. Not eligible as rewrite method performance rows.

Denominator eligibility: may reference `controls_360.csv`. Must not use Track A rewrite denominator IDs for hard-negative controls.

## `rewrite_candidate_cell`

Represents: `case x engine x same-engine route/method x candidate_id`.

Required fields: `case_id`, `pool`, `case_set`, `denominator_id`, `engine`, `route=same_engine_rewrite`, `method_role`, `candidate_id`, `source_sql_path`, `candidate_sql_path`, `generated`, `ready`, `executed`, `exact`, `timed`, `result_status`, `evidence_source`, `notes`.

Forbidden or discouraged fields: none, but `latency_ms`, `speedup`, and `timing_eligible` must remain null or pending until timing evidence and metric definitions are approved.

Metric eligibility: future correctness and performance metrics when denominator eligible and final metrics contract allows.

Denominator eligibility: Track A same-engine rows only when joined to `denominator_same_engine_120.csv`.

## `plan_observability_artifact`

Represents: `case x engine x route/control/method x artifact_id`.

Required fields: `case_id` when known, `case_set`, `engine` when known, `route=plan_observability`, `method_role`, `candidate_id` as artifact ID until schema adds `artifact_id`, `plan_available`, `plan_artifact_path`, `evidence_source`, `retained_artifact_path`, `notes`.

Forbidden or discouraged fields: `speedup`, `latency_ms`, `timed`, and `timing_eligible` should be null unless the artifact is explicitly linked to a candidate row and metrics contract permits use.

Metric eligibility: eligible for observability metrics only.

Denominator eligibility: not a speedup or same-engine rewrite denominator row.

## `portability_candidate_cell`

Represents: `PORT case x source/target engine x portability route x candidate_id`.

Required fields: `case_id`, `pool=PORT`, `case_set`, `engine`, `route=portability`, `method_role`, `candidate_id`, `source_sql_path`, `candidate_sql_path`, `generated`, `ready`, `executed`, `exact`, `result_status`, `checker_status`, `evidence_source`, `notes`.

Forbidden or discouraged fields: same-engine Track A denominator IDs unless a future contract explicitly maps the portability route to a separate denominator.

Metric eligibility: eligible only for future cross-engine executable or consistency reporting, not Track A same-engine performance.

Denominator eligibility: separate PORT portability semantics. Must not be mixed with same-engine Track A rows.

## `verifier_support_pair`

Represents: `SQL pair x verifier tool x support result`.

Required fields: `case_id` when known, `case_set`, `route=verifier_support`, `method_role=verifier_support`, `candidate_id` as support-pair ID, `result_status`, `checker_status` or support status where applicable, `evidence_source`, `retained_artifact_path`, `notes`.

Forbidden or discouraged fields: `denominator_id`, `latency_ms`, `speedup`, and `timing_eligible` should be null.

Metric eligibility: support evidence only.

Denominator eligibility: not a rewrite-generation baseline and not same-engine speedup denominator.

## `retained_summary_artifact`

Represents: summary table, paper-facing retained artifact, frozen evidence summary, index, or comparison target.

Required fields: `case_set`, `route=summary` or specific support route, `method_role=retained_legacy_reference`, `candidate_id` as summary/artifact ID, `evidence_source`, `retained_artifact_path`, `notes`.

Forbidden or discouraged fields: `denominator_id`, `latency_ms`, `speedup`, `exact`, and `timed` should not be used as canonical row values.

Metric eligibility: not a metric row by default.

Denominator eligibility: reference-only unless a future adapter parses it into lower-grain rows.

## `user_run_candidate_cell`

Represents: external user-submitted candidate SQL under the public runner output policy.

Required fields: `case_id`, `pool`, `case_set`, `denominator_id` if benchmark-scoped, `engine`, `route`, `method_role=user_candidate`, `candidate_id`, `source_sql_path`, `candidate_sql_path`, `generated`, `ready`, `executed`, `exact`, `timed`, `result_status`, `evidence_source=user_run`, `notes`.

Forbidden or discouraged fields: case-local `runs/` paths in `retained_artifact_path`.

Metric eligibility: future user-facing metrics only after runner/output policy and metrics contract are approved.

Denominator eligibility: only for approved benchmark-scoped submissions.

## Support-only Evidence

The following are support-only unless a later contract explicitly changes scope:

- `plan_observability_artifact`
- `verifier_support_pair`
- `retained_summary_artifact`
- raw log/archive references

Support-only evidence cannot enter rewrite performance denominators.

## Paper-facing Summary Artifacts

Paper-facing retained summaries are traceability and comparison targets. They do not become canonical metric rows until a future adapter parses them into lower-grain ledger rows and the metric contract approves aggregation.

## Future User-run Rows

User-run rows must follow the public runner output policy. They must write outputs outside case-local `runs/` and must not alter retained evidence.
