# Retained Evidence Adapter Gap Report

## Directly Available Fields

The retained candidate map directly provides source artifact references, evidence roles, broad case or scope labels, broad pool labels, related method/route strings, broad denominator scope, recommended public action, `copy_now=false`, manual-review flags, and notes.

The aligned release repository directly provides fixed Common-core v0 membership, case package paths, canonical package status, validator status, planned denominator scaffolds, and planned control scaffolds.

These inputs can directly support:

- `case_set`
- `evidence_source`
- `retained_artifact_path`
- `notes`
- initial `method_role` and `route` labels after normalization

## Fields Requiring Parsing Adapters

The following fields require artifact-specific parsers before they can be populated safely:

- `executed`
- `exact`
- `result_status`
- `failure_stage`
- `failure_type`
- `checker_status`
- `plan_available`
- `plan_artifact_path`
- `latency_ms`
- `speedup`
- `timed`
- `timing_eligible`

Candidate rows identify artifact groups, not normalized row-level evidence facts. Parsing adapters must preserve failed, unsupported, missing-artifact, timing-missing, and checker-rejected states rather than collapsing them.

## Fields Requiring Case Manifest Lookup

The following fields need canonical case package or inventory lookup:

- `case_id`
- `pool`
- `source_sql_path`
- `candidate_sql_path` for canonical source/positive/hard-negative controls

Mixed-scope retained artifacts must not be assigned to a case unless the artifact content or a future parser provides row-level evidence.

## Fields Requiring Case-set Denominator Lookup

The following fields require joins to `case_sets/common_core_v0/denominator_same_engine_120.csv` or `controls_360.csv`:

- `denominator_id`
- `engine`
- `route`

Legacy denominator references may be used to crosscheck scaffolds, but they must not update denominator values.

## Fields Requiring Metrics Finalization

The following fields are especially blocked on final metric definitions:

- `exact`
- `timed`
- `latency_ms`
- `speedup`
- `timing_eligible`
- parseability/extractability/runnable SQL statuses
- fallback/regression categories
- observability metric wording

Existing retained artifacts may contain values or prior summaries, but this task does not authorize using them as final public metrics.

## Fields Not Available From Retained Evidence Alone

The retained candidate map alone does not provide:

- stable `candidate_id` values;
- canonical row-grain decisions;
- public-safe copied artifact paths;
- final user submission identifiers;
- final output root paths;
- definitive metric eligibility gates.

These must be created by future adapter and runner design after approval.

## Risks If Implemented Too Early

Implementing metrics or report rendering before the ledger and metric contract are approved risks:

- silently changing denominator treatment;
- treating legacy paper tables as the canonical data model;
- collapsing route-specific evidence into a leaderboard;
- publishing raw logs or local paths;
- recomputing speedup from ambiguous timing rows;
- mixing verifier support with rewrite-generation baselines;
- writing new outputs into case-local `runs/`.
