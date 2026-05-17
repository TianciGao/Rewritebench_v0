# Retained Evidence Adapter Design v1 Draft

Status: draft design and validation plan, not implementation-authorizing

Purpose: define how existing retained evidence should later be adapted into the evidence ledger governed by Metrics Contract v1 and the row-grain policy.

This draft does not implement adapters, compute metrics, create scripts, create source package code, render paper tables, copy reports/results, run DB engines, run validation scripts, run LLM calls, run timing workloads, update denominator values, change paper results, change case membership, modify case packages, or modify raw legacy evidence.

## Inputs

Primary release inputs:

- `case_sets/common_core_v0/cases.csv`
- `case_sets/common_core_v0/denominator_same_engine_120.csv`
- `case_sets/common_core_v0/controls_360.csv`
- `inventory/case_registry.csv`
- `inventory/source_registry.csv`
- canonical case package manifests and `evidence/runs_retention.yaml`

Primary retained-evidence maps:

- `audits/reports_results_retained_evidence_map/reports_results_artifact_inventory.csv`
- `audits/reports_results_retained_evidence_map/retained_evidence_candidate_map.csv`
- `audits/retained_evidence_ledger_mapping/common_core_ledger_source_inventory.csv`
- `audits/retained_evidence_ledger_mapping/retained_evidence_to_ledger_field_map.csv`

Legacy reports/results remain reference inputs only. Adapters must not copy them or mutate them.

## Non-goals

- No metric computation.
- No speedup recomputation.
- No paper table rendering.
- No reports/results migration.
- No public runner output implementation.
- No writes to case-local `runs/`.
- No denominator or case membership changes.
- No raw legacy evidence changes.

## Adapter Families

`legacy_reports_adapter`: reads curated legacy report and paper-freeze artifacts from the retained-evidence maps and emits typed ledger rows only when row grain is explicit.

`retained_results_adapter`: parses selected retained result summaries into `rewrite_candidate_cell`, `portability_candidate_cell`, or `retained_summary_artifact` rows after public-safe artifact selection.

`case_runs_adapter`: reads canonical case package `evidence/runs_retention.yaml` files and public-safe retained case evidence summaries. It must not write into case-local `runs/`.

`plan_observability_adapter`: maps sanitized plan evidence and plan availability references into `plan_observability_artifact` rows and support fields for attribution.

`hard_negative_control_adapter`: maps expected rejection and checker-control evidence into `control_cell` rows joined to `controls_360.csv`.

`portability_packet_adapter`: maps PORT retained evidence into `portability_candidate_cell` rows under cross-engine/generalization semantics. It must not mix these rows with Track A same-engine rows.

`verifier_support_adapter`: maps SQLSolver, VeriEQL, or similar retained support evidence into `verifier_support_pair` rows. These are correctness support rows, not rewrite-generation baselines.

`timing_record_adapter`: maps timing references into timing fields only after timing eligibility rules are approved. It must preserve `timing_missing` and `target_timing_missing`.

`retained_summary_adapter`: records paper-facing retained artifacts, paper summary tables, denominator references, raw-log references, and archive-only groups as `retained_summary_artifact` rows or manual-review references.

## Output Record Types

Adapters may emit only these draft record types:

- `control_cell`
- `rewrite_candidate_cell`
- `plan_observability_artifact`
- `portability_candidate_cell`
- `verifier_support_pair`
- `retained_summary_artifact`
- `user_run_candidate_cell`

`user_run_candidate_cell` is included for future schema compatibility. Retained-evidence adapters should not emit user-run rows unless a later public runner task authorizes user-run ingestion.

## Row-grain Policy

Every adapter output row must have an explicit `record_type`.

Candidate grain:

`case_id x engine x route x method_role x candidate_id x denominator_id x evidence_source`

Control grain:

`case_id x engine x control_route x control_id x evidence_source`

Artifact grain:

`case_id_or_scope x engine_if_known x route_or_method_if_known x artifact_id x evidence_source`

If an artifact cannot be parsed into an approved row grain without guessing, the adapter must emit a `retained_summary_artifact` row or mark the artifact `manual_review_required`.

## Denominator Joins

Adapters must load membership and denominator context before parsing retained evidence.

Required joins:

- fixed case membership from `case_sets/common_core_v0/cases.csv`;
- Track A same-engine denominator IDs from `denominator_same_engine_120.csv`;
- control IDs from `controls_360.csv`;
- case facts from `inventory/case_registry.csv`;
- source family context from `inventory/source_registry.csv` when useful for descriptions;
- canonical case manifest paths for `source_sql_path` and control SQL paths.

Adapters must not create denominator rows. Legacy denominator artifacts may be crosschecked against release scaffolds, but they must not update denominator values.

## Denominator Boundaries

Adapters must not mix:

- same-engine rewrite candidate rows;
- source and positive control rows;
- hard-negative control rows;
- PORT portability rows;
- verifier support pairs;
- plan observability artifacts;
- retained summary artifacts;
- future user-submitted rows.

No adapter output may create or support a global leaderboard.

## N.A. And Unsupported Handling

Adapters must preserve explicit missingness and non-applicability. They should use stable statuses such as:

- `unsupported`
- `not_applicable`
- `unknown`
- `timing_missing`
- `verifier_unknown`
- `target_timing_missing`
- `evidence_not_retained`
- `manual_review_required`
- `blocked`

Blank, null, or missing fields must not be interpreted as false or zero without an explicit adapter rule.

## Metrics Contract v1 Support

Adapter outputs should support Metrics Contract v1 without computing metrics.

Primary metrics and required row families:

- Generation Rate: `rewrite_candidate_cell`, future `user_run_candidate_cell`.
- Execution Coverage Rate: `rewrite_candidate_cell`, future `user_run_candidate_cell`.
- Result Consistency Rate: `rewrite_candidate_cell`.
- Semantic Equivalence Rate: `rewrite_candidate_cell` plus `verifier_support_pair`.
- GM_Speedup: `rewrite_candidate_cell` with result-consistent timed evidence.
- Speedup Ratio Percentiles: `rewrite_candidate_cell` with result-consistent timed evidence.
- Attribution Coverage: attribution-eligible rows plus `plan_observability_artifact`, `control_cell`, and `verifier_support_pair` support.
- Cross-Engine Execution: `portability_candidate_cell`.
- Cross-Engine Consistency: `portability_candidate_cell`.
- Speedup Retention: paired `portability_candidate_cell` rows with source and target timing.

Diagnostic fields:

- extraction/readiness;
- parseability;
- runnable SQL status;
- failure buckets;
- `Regression@20` legacy diagnostic;
- PlanFrontier and plan artifact support;
- verifier support evidence.

## Validation Gates

Before any future metrics computation, adapter output must pass:

- input manifest validation;
- row count checks;
- stable ID uniqueness checks;
- required-field completeness checks;
- record-type-specific field checks;
- denominator scaffold join checks;
- control scaffold join checks;
- case registry and manifest path checks;
- explicit missingness checks;
- no-global-leaderboard checks;
- no metric computation checks;
- no reports/results mutation checks;
- no case-local `runs/` output checks;
- public hygiene checks for any public output paths.

## Implementation Sequence

1. Define ledger schema model and validation fixtures.
2. Implement `retained_summary_adapter` first because summary rows are lowest risk and do not enter metric denominators.
3. Implement `control_cell` and hard-negative control adapters.
4. Implement `rewrite_candidate_cell` adapters for same-engine retained evidence.
5. Implement timing adapters only after timing eligibility tests and speedup policy are approved.
6. Implement portability and verifier support adapters.
7. Implement metrics computation only after adapter validation and explicit authorization.
8. Implement paper table rendering only after metrics validation and explicit authorization.
9. Implement public runner outputs last under the public output policy.

## Implementation Boundary

This design is an implementation plan only. Future code must be introduced by a separate implementation task and must preserve denominator values, paper results, case membership, raw legacy evidence, and the no-global-leaderboard rule.
