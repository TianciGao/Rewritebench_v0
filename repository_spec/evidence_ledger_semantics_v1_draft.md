# Evidence Ledger Semantics v1 Draft

Status: draft policy layer, not implementation-authorizing

Purpose: define field semantics for the future SQL-RewriteBench evidence ledger before retained-evidence adapters, metrics computation, report rendering, reproduction CLI, or public runner outputs are implemented.

This draft does not compute metrics, change denominator values, change paper results, update paper tables, copy reports/results, authorize adapters, or authorize the reproduction interface.

## Ledger Row Philosophy

The evidence ledger uses a typed long format. Each row represents one evidence-bearing observation, not a wide paper table and not a leaderboard row.

Every row must have a `record_type` discriminator. `record_type` is a required policy field introduced by this semantics layer and should be added to the next schema revision. The 28 fields in `evidence_ledger_schema_v1_draft.md` remain the draft common field set reviewed by this task.

Rows must preserve denominator, route, method role, evidence source, and failure boundaries. Missing, failed, unsupported, checker-rejected, timing-missing, and archive-only states must be represented explicitly rather than dropped.

## Typed Long Format

Allowed draft `record_type` values:

- `control_cell`
- `rewrite_candidate_cell`
- `plan_observability_artifact`
- `portability_candidate_cell`
- `verifier_support_pair`
- `retained_summary_artifact`
- `user_run_candidate_cell`

Record types must not be mixed into one global leaderboard. A plan artifact, verifier support pair, retained paper summary, hard-negative control, and same-engine rewrite candidate answer different questions.

## Required Common Fields

All ledger rows should carry:

- `record_type`
- `case_set`
- `evidence_source`
- `retained_artifact_path` or a future output artifact path
- `notes`

Rows tied to a fixed Common-core case should also carry:

- `case_id`
- `pool`
- `engine` when engine-specific
- `route`

Rows that participate in a planned denominator must carry `denominator_id`. Rows that are support-only or summary-only must leave `denominator_id` null or set it to a non-metric reference identifier, never to a Track A denominator row.

## Field Semantics

| Field | Meaning | Allowed values or type | Required or nullable | Applies to record types | Denominator effect | Depends on final metric definition |
|---|---|---|---|---|---|---|
| `case_id` | Canonical case identifier. | Common-core case ID such as `PERF_0006`; nullable for summary-only rows. | Required for case-scoped rows. | all except mixed `retained_summary_artifact` | Identifies denominator membership but does not create it. | no |
| `pool` | Case pool. | `PERF`, `CONS`, `PORT`, `LONGTAIL`; nullable for mixed summaries. | Required when `case_id` is set. | all case-scoped record types | No denominator effect by itself. | no |
| `case_set` | Release case set. | `common_core_v0` for this scope. | Required. | all | Selects membership namespace only. | no |
| `denominator_id` | Stable planned denominator row or reference. | `track_a_same_engine:<case_id>:<engine>` for Track A rows; control IDs for controls; null for support-only rows. | Required for denominator-eligible candidate rows. | `control_cell`, `rewrite_candidate_cell`, `portability_candidate_cell` when applicable, `user_run_candidate_cell` when benchmark-scoped | Determines denominator join but does not imply result success. | no |
| `engine` | Engine observed by the row. | `postgres`, `mysql`, `spark`; nullable for mixed summaries or non-engine support. | Required for engine-specific rows. | all case-scoped engine rows | Part of Track A and control denominator identity. | no |
| `route` | Evidence route. | `source`, `positive`, `hard_negative`, `same_engine_rewrite`, `portability`, `plan_observability`, `verifier_support`, `summary`, or future approved route. | Required. | all | Routes separate denominators and support evidence. | no |
| `method_role` | Role-aware method or evidence label. | `control`, `direct_llm`, `repair_1`, `sqlglot`, `calcite_hep`, `r_bot`, `verifier_support`, `retained_legacy_reference`, `user_candidate`, or approved role. | Required. | all | Determines metric slice; not a denominator by itself. | no |
| `candidate_id` | Stable candidate/control/user submission identifier. | Adapter-generated stable ID; control IDs may be deterministic. | Required for candidate/control rows; nullable for summary artifacts. | `control_cell`, `rewrite_candidate_cell`, `portability_candidate_cell`, `user_run_candidate_cell` | Prevents duplicate row collapse. | no |
| `source_sql_path` | Canonical source SQL path. | Repository-relative path; nullable if not case-scoped. | Required for candidate/control rows after case lookup. | `control_cell`, `rewrite_candidate_cell`, `portability_candidate_cell`, `user_run_candidate_cell` | No denominator effect. | no |
| `candidate_sql_path` | Candidate, control, positive, negative, or user SQL path. | Repository-relative path or output-root path; nullable for summary or unavailable rows. | Required when SQL exists; null if missing. | candidate/control rows | No denominator effect. | no |
| `generated` | Whether SQL was generated by a method or user, not a fixed case control. | boolean or `unknown`. | Required for candidate rows. | `rewrite_candidate_cell`, `portability_candidate_cell`, `user_run_candidate_cell` | Can affect generation/readiness metrics. | no |
| `ready` | Whether row reached the relevant downstream gate. | boolean or `unknown`. | Required for candidate rows after adapter parse. | candidate rows | Readiness denominator must remain distinct from execution denominator. | yes for final readiness naming |
| `parse_status` | SQL parse/extractability status. | `parsed`, `not_parsed`, `not_applicable`, `unknown`, future approved statuses. | Nullable until parser exists. | candidate rows | Does not change planned denominator; may support future parse metrics. | yes |
| `executed` | Whether execution happened for this evidence row. | boolean or `unknown`. | Required for execution-relevant candidate/control rows. | `control_cell`, `rewrite_candidate_cell`, `portability_candidate_cell`, `user_run_candidate_cell` | Execution coverage is separate from planned denominator. | no |
| `exact` | Whether correctness gate passed for the row. | boolean, `not_applicable`, or `unknown`. | Required for correctness-relevant rows after adapter parse. | candidate/control rows | Exact denominator is a filtered metric slice, not a new membership list. | yes |
| `timed` | Whether usable timing evidence is present. | boolean, `not_applicable`, or `unknown`. | Required for performance-eligible rows after adapter parse. | candidate rows | Timed rows are a performance slice only. | yes |
| `result_status` | Normalized row outcome. | `pass`, `fail`, `unsupported`, `missing_artifact`, `not_run`, `checker_rejected`, `timing_missing`, `unknown`, or approved status. | Required after adapter parse. | all except pure summaries | Used for reporting state, not membership. | no |
| `failure_stage` | Stage where failure or missingness occurred. | `generation`, `parse`, `execution`, `checker`, `plan_collection`, `timing`, `artifact_collection`, `not_applicable`, `unknown`. | Nullable for success rows. | candidate/control/artifact rows | No denominator effect. | no |
| `failure_type` | Stable failure bucket. | controlled vocabulary TBD; may be `unknown`. | Nullable until bucket policy exists. | candidate/control/artifact rows | No denominator effect. | no |
| `checker_status` | Checker or hard-negative outcome. | `pass`, `reject_expected`, `reject_unexpected`, `not_applicable`, `not_run`, `unknown`. | Required where a checker applies. | `control_cell`, `rewrite_candidate_cell`, `portability_candidate_cell`, `user_run_candidate_cell` | Supports correctness gate; does not change membership. | no |
| `plan_available` | Whether plan evidence exists. | boolean, `not_applicable`, or `unknown`. | Required for plan artifact rows; nullable elsewhere. | all, especially `plan_observability_artifact` | Observability metric only. | no |
| `plan_artifact_path` | Public-safe plan artifact or archive reference. | repository-relative path, output-root path, archive reference, or null. | Required for `plan_available=true`. | `plan_observability_artifact` and plan-linked rows | No speedup denominator effect. | no |
| `latency_ms` | Retained or future measured latency in milliseconds. | numeric positive value or null. | Nullable. | performance-eligible candidate rows | Only interpretable on exact and timed rows. | yes |
| `speedup` | Derived speedup value. | numeric value or null. | Nullable. | performance-eligible candidate rows | Must not be recomputed until metrics contract is final. | yes |
| `timing_eligible` | Whether timing interpretation is allowed. | boolean, `not_applicable`, or `unknown`. | Required before performance reporting. | candidate rows | Defines performance slice, not planned denominator. | yes |
| `evidence_source` | Source class for row evidence. | `canonical_case_package`, `retained_legacy_report`, `retained_legacy_run`, `adapter_import`, `user_run`, `manual_summary`. | Required. | all | No denominator effect. | no |
| `retained_artifact_path` | Source or retained artifact supporting the row. | repository path, legacy reference, archive reference, output-root path, or null. | Required for retained rows. | all retained row types | Traceability only. | no |
| `notes` | Boundary, ambiguity, or caveat text. | free text. | Required when any field is unknown, ambiguous, or pending definition. | all | No denominator effect. | no |

## Status Fields

Status fields include `generated`, `ready`, `parse_status`, `executed`, `exact`, `timed`, `result_status`, `checker_status`, `plan_available`, and `timing_eligible`.

Adapters must preserve `unknown`, `not_applicable`, and missing-artifact states. Null or blank must not mean false unless the adapter explicitly sets false.

## Failure Fields

`failure_stage` and `failure_type` explain why a row did not advance. They are not metrics by themselves. They must be populated conservatively and may require manual review for raw logs or ambiguous legacy artifacts.

## Timing Fields

`timed`, `latency_ms`, `speedup`, and `timing_eligible` are performance fields. They remain interpretation-blocked until the metrics contract is finalized. Blank timing is not zero. Speedup must not be recomputed in a semantics or adapter task.

## Plan Fields

`plan_available` and `plan_artifact_path` support observability reporting. Plan rows and plan-linked fields must not be used as speedup denominator rows.

## Evidence And Provenance Fields

`evidence_source`, `retained_artifact_path`, and `notes` preserve traceability and public-safety boundaries. Archive-only, raw-log, private, or mixed-scope artifacts may be represented as support/reference rows, but not as metric rows.

## Denominator Boundary Fields

`case_set`, `denominator_id`, `engine`, `route`, `method_role`, and `record_type` jointly determine whether a row can be considered by a future metric. No row can change Common-core membership or denominator values.

## Explicitly Not Authorized

This semantics draft does not authorize:

- retained-evidence adapter implementation;
- metrics computation;
- paper table rendering;
- reports/results migration;
- DB validation;
- evidence regeneration;
- timing reruns;
- unified reproduction CLI or public runner implementation;
- denominator or case membership changes.

## Relation To Metrics Contract

This document defines row semantics. `metrics_contract_v1_draft.md` still controls which rows may be aggregated into metrics. Metrics that depend on final definitions remain blocked until maintainer/team approval.
