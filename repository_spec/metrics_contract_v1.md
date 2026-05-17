# Metrics Contract v1

Status: formal contract, not implementation-authorizing

Purpose: define the SQL-RewriteBench public workbench metric contract from the maintainer/team-approved paper scope.

This contract formalizes metric names, layers, denominators, eligibility rules, diagnostic boundaries, and non-computable conditions. It does not implement metric computation, retained-evidence adapters, paper table rendering, reports/results migration, DB validation, timing reruns, evidence regeneration, denominator updates, paper result updates, case membership changes, or a global leaderboard.

## Scope And Fixed Boundaries

- Public v0 benchmark line: Common-core v0.
- Common-core case count: 40 cases.
- Track A same-engine planned denominator: 120 planned case-engine candidate opportunities.
- Engines: PostgreSQL, MySQL, Spark.
- Benchmark unit: case package.
- Reporting must be case-aware, engine-aware, method-aware, role-aware, and denominator-aware.
- Public wording should use "cases" where that avoids confusion with ledger rows.
- Public wording should use "rewrite method" where appropriate instead of "rewrite route."
- No global leaderboard is allowed.
- Hard negatives are checker controls, not method-generated failures.
- Verifier evidence is folded into correctness and semantic-equivalence support; it is not an independent metric layer or rewrite-generation baseline.
- Performance metrics apply only to result-consistent timed cases.

## Metric Layers

| Layer | Primary metric |
|---|---|
| Coverage | Generation Rate |
| Coverage | Execution Coverage Rate |
| Correctness | Result Consistency Rate |
| Correctness | Semantic Equivalence Rate |
| Performance | GM_Speedup |
| Performance | Speedup Ratio Percentiles |
| Explainability | Attribution Coverage |
| Generalization | Cross-Engine Execution |
| Generalization | Cross-Engine Consistency |
| Generalization | Speedup Retention |

## Coverage Metrics

### Generation Rate

Definition: fraction of planned cases for which a rewrite method emits candidate SQL.

Formula:

`Generation Rate = generated_candidate_cases / planned_candidate_cases`

Denominator: approved planned candidate cases for the method and scope, such as the Track A same-engine case-engine denominator for same-engine rewrite methods.

Record types used: `rewrite_candidate_cell`; future public submissions may use `user_run_candidate_cell`.

Eligibility:

- A case counts in the numerator when candidate SQL is emitted for the planned method/scope.
- Candidate SQL generation is the only primary Generation Rate meaning in v1.

Diagnostic boundary:

- SQL extraction, readiness, parseability, runnable SQL status, preflight status, and no-candidate status may be retained as diagnostic ledger fields or optional ready-rate fields.
- These diagnostics are not second primary Generation Rate variants.

N.A. conditions: report `N.A.` only when a method/scope has no approved planned candidate denominator.

### Execution Coverage Rate

Definition: fraction of planned candidate cases that reach execution under the applicable method and scope.

Formula:

`Execution Coverage Rate = executed_candidate_cases / planned_candidate_cases`

Denominator: the same approved planned candidate cases used for the coverage scope.

Record types used: `rewrite_candidate_cell`; future public submissions may use `user_run_candidate_cell`.

Eligibility:

- A case counts in the numerator when execution was attempted or completed according to the approved execution-status policy.
- Unsupported, not-run, preflight-blocked, missing-candidate, and execution-failed states must be reported transparently and must not be silently dropped.

N.A. conditions: report `N.A.` when execution is outside the approved scope for the method or engine.

## Correctness Metrics

### Result Consistency Rate

Definition: fraction of executed candidate cases whose observed result is consistent with the expected result under the checker or retained result-comparison protocol.

Formula:

`Result Consistency Rate = result_consistent_cases / executed_candidate_cases`

Denominator: executed candidate cases for the approved method and scope.

Record types used: `rewrite_candidate_cell`; `control_cell` may support package/control reporting but is not a rewrite-method candidate denominator.

Eligibility:

- Candidate must be executed.
- Candidate must have a comparable result or checker outcome.
- Result consistency is an execution-evidence correctness metric; it does not by itself claim formal semantic proof.

N.A. conditions:

- Report `N.A.` when no candidate cases reached execution for the method/scope.
- Unsupported or not-run cases are excluded from the executed denominator but should remain visible in coverage diagnostics.

### Semantic Equivalence Rate

Definition: fraction of verifier-decidable, result-consistent candidate cases for which semantic equivalence is established by an approved semantic-equivalence basis.

Formula:

`Semantic Equivalence Rate = semantically_equivalent_cases / verifier_decidable_result_consistent_cases`

Denominator: result-consistent cases for which the approved verifier or semantic-equivalence basis is applicable and decidable.

Record types used: `rewrite_candidate_cell` with `verifier_support_pair` as support evidence.

Eligibility:

- Candidate must be result-consistent.
- Candidate must be in the verifier-decidable/applicable subset.
- Unknown, undecidable, unsupported, or no-verifier-support cases are reported separately.

N.A. conditions:

- Report `N.A.` when no cases in the scope are verifier-decidable/applicable.
- Do not count unknown or undecidable cases as failures unless a later approved policy says so.

## Performance Metrics

### GM_Speedup

Definition: geometric mean speedup over result-consistent timed candidate cases.

Formula:

`GM_Speedup = geometric_mean(speedup_ratio for result_consistent_timed_cases)`

Denominator: result-consistent timed candidate cases.

Record types used: `rewrite_candidate_cell`.

Eligibility:

- Candidate must be result-consistent.
- Candidate must have usable timing evidence.
- Timing must be eligible under the approved timing policy.
- Missing timing is not zero.

N.A. conditions:

- Report `N.A.` when no result-consistent timed cases exist for the method/scope.

### Speedup Ratio Percentiles

Definition: percentile summary of speedup ratios over result-consistent timed candidate cases.

Formula:

Report approved percentiles such as P25, median/P50, P75, and optionally IQR or additional approved percentiles over the speedup-ratio set.

Denominator: result-consistent timed candidate cases.

Record types used: `rewrite_candidate_cell`.

Eligibility:

- Same as `GM_Speedup`.
- Every percentile table should report the number of result-consistent timed cases.

N.A. conditions:

- Report `N.A.` when no result-consistent timed cases exist for the method/scope.

Legacy diagnostic:

- `Regression@20` is no longer the primary performance-regression metric.
- `Regression@20` may remain only as a legacy diagnostic/comparison if explicitly needed for continuity.

## Explainability Metrics

### Attribution Coverage

Definition: fraction of attribution-eligible cases with sufficient operator-level attribution evidence from structured plan/SQL analysis.

Formula:

`Attribution Coverage = attribution_supported_cases / attribution_eligible_cases`

Denominator: attribution-eligible cases for the approved method/scope. The exact implementation schema and eligible denominator must be defined before computation.

Record types used: likely `rewrite_candidate_cell`, `plan_observability_artifact`, `control_cell`, and `verifier_support_pair`, depending on the approved attribution schema.

Eligibility:

- Attribution evidence should connect a rewrite decision or semantic/performance-relevant change to structured SQL and/or public-safe plan evidence.
- Attribution must not overclaim internal optimizer reasoning.
- LLM-proposed attribution is not sufficient unless supported by retained evidence or human verification.

N.A. conditions:

- Report `N.A.` when attribution evidence is outside scope or the attribution denominator is not defined.

Support boundary:

- The atom-based Rewrite Opportunity Observability Score is a pilot/support design, not the main metric unless separately approved.
- PlanFrontier and plan artifacts remain support/diagnostic evidence, not the main explainability metric.

## Generalization Metrics

### Cross-Engine Execution

Definition: fraction of approved cross-engine candidate cases that execute on the target engine.

Formula:

`Cross-Engine Execution = target_engine_executed_cases / approved_cross_engine_candidate_cases`

Denominator: approved cross-engine candidate cases under portability/generalization scope. This is separate from Track A same-engine denominators.

Record types used: `portability_candidate_cell`.

N.A. conditions: report `N.A.` when a target engine or portability scope is unsupported or lacks an approved denominator.

### Cross-Engine Consistency

Definition: fraction of executed cross-engine candidate cases that produce target-engine results consistent with the approved cross-engine checking protocol.

Formula:

`Cross-Engine Consistency = cross_engine_consistent_cases / target_engine_executed_cases`

Denominator: executed cross-engine candidate cases unless a later approved protocol uses an approved planned portability denominator.

Record types used: `portability_candidate_cell`.

N.A. conditions: report `N.A.` when no target-engine execution cases exist for the scope.

### Speedup Retention

Definition: retained speedup ratio across paired source-engine and target-engine timing evidence.

Formula:

Implementation must define the paired source/target calculation before computation. At minimum, both source and target sides must be result-consistent and timed.

Denominator: paired source-engine and target-engine candidate cases with result-consistent timing on both sides.

Record types used: paired `portability_candidate_cell` rows.

N.A. conditions:

- Report `N.A.` when paired target-engine timing does not exist, is unsupported, or is outside the approved protocol.
- Missing paired timing is not zero and is not a speedup-retention failure unless a later approved policy says so.

## Diagnostic And Support Fields

The following remain diagnostic/support unless a later approved contract promotes them:

- failure bucket distribution;
- SQL extraction status;
- parseability;
- runnable SQL status;
- readiness/ready rate;
- unsupported status;
- preflight-blocked status;
- source-like/no-op status;
- PlanAvailability;
- PlanFrontier / plan observability summaries;
- atom-based Rewrite Opportunity Observability Score;
- verifier support counts outside Semantic Equivalence Rate.

Failure buckets are diagnostic only. `Candidate Failure Rate` is removed as a primary metric.

## Renamed, Removed, Or Demoted Metrics

| Older name | v1 status |
|---|---|
| Generatable Rate | renamed to Generation Rate |
| Exact Correctness Rate | renamed to Result Consistency Rate |
| Speedup Distribution | renamed to Speedup Ratio Percentiles |
| Regression@20 | removed as primary; optional legacy diagnostic only |
| Candidate Failure Rate | removed as primary; failure buckets diagnostic only |
| Observability / PlanFrontier | replaced in primary suite by Attribution Coverage |
| Support Layer | removed as independent layer; verifier evidence folded into correctness |

Public table-column wording should prefer `Description` over `Interpretation`.

## Record Type Boundaries

- `rewrite_candidate_cell`: same-engine rewrite candidate metrics.
- `control_cell`: source/positive/hard-negative controls and checker guard evidence; not rewrite-method performance denominator rows.
- `portability_candidate_cell`: cross-engine/generalization metrics; not Track A same-engine rows.
- `plan_observability_artifact`: support/diagnostic explainability evidence.
- `verifier_support_pair`: correctness/semantic-equivalence support only.
- `retained_summary_artifact`: traceability or comparison target, not a canonical metric row by default.
- `user_run_candidate_cell`: future user submissions after public runner policy is implemented.

## Implementation Status

Formalized metrics contract: yes.

Metrics implementation authorized: no.

Retained-evidence adapter implementation authorized: no.

Unified reproduction CLI implementation authorized: no.

Public runner implementation authorized: no.

Paper table rendering authorized: no.

Reports/results migration authorized: no.

Any future implementation must first define adapter row materialization, validate denominator joins, preserve diagnostic states, and maintain no-global-leaderboard reporting.
