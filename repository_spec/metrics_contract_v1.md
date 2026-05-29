# Metrics Contract v1

Status: formal contract, D032/D033-aligned, not official-metrics implementation-authorizing

Purpose: define the SQL-RewriteBench public workbench metric contract from the D032 latest paper metric table and D033 local metrics boundary decision.

This contract formalizes metric names, layers, denominators, eligibility rules, diagnostic boundaries, and non-computable conditions. It does not implement new metric computation, retained-evidence adapters, POCR adapters, paper table rendering, reports/results migration, DB validation, timing reruns, verifier runs, evidence regeneration, denominator updates, paper result updates, case membership changes, or a global leaderboard.

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
- Performance metrics apply only to strict exact/result-consistent timed cases.
- Current local metric outputs are non-official local diagnostic metrics and must not be treated as paper results.

## Metric Layers

| Layer | Primary metric |
|---|---|
| Coverage | Generation Rate |
| Coverage | Execution Coverage Rate |
| Correctness | Result Consistency Rate |
| Correctness | Semantic Equivalence Rate |
| Performance | GM Speedup Ratio |
| Performance | Speedup Ratio Percentiles |
| Interpretability | Positive Operation Coverage Rate |
| Generalization | Cross-Engine Execution Coverage Rate |
| Generalization | Cross-Engine Result Consistency Rate |
| Generalization | Cross-Engine GM Speedup Ratio |

## Coverage Metrics

### Generation Rate

Definition: fraction of selected/planned cases for which a rewrite method emits candidate SQL.

Formula:

`Generation Rate = candidate_generated / selected`

Paper notation: `|G_r| / N_S`

Denominator: selected/planned candidate cases for the approved method and scope, such as the Track A same-engine case-engine denominator for same-engine rewrite methods.

Record types used: `rewrite_candidate_cell`; future public submissions may use `user_run_candidate_cell`.

Eligibility:

- A case counts in the numerator when candidate SQL is emitted for the planned method/scope.
- Candidate SQL generation is the only primary Generation Rate meaning in v1.

Diagnostic boundary:

- SQL extraction, readiness, parseability, runnable SQL status, preflight status, and no-candidate status may be retained as diagnostic ledger fields or optional ready-rate fields.
- `preflight_passed` is a funnel diagnostic and is not the Generation Rate numerator.
- These diagnostics are not second primary Generation Rate variants.

N.A. conditions: report `N.A.` only when a method/scope has no approved planned candidate denominator.

### Execution Coverage Rate

Definition: fraction of selected/planned candidate cases whose generated candidate SQL executes successfully under the applicable method and scope.

Formula:

`Execution Coverage Rate = candidate_executable / selected`

Paper notation: `|E_r| / N_S`

Denominator: the same approved planned candidate cases used for the coverage scope.

Record types used: `rewrite_candidate_cell`; future public submissions may use `user_run_candidate_cell`.

Eligibility:

- A case counts in the numerator when candidate execution succeeds according to the approved execution-status policy.
- `source_executable` is an environment/source guard diagnostic and is not the Execution Coverage numerator.
- Unsupported, not-run, preflight-blocked, missing-candidate, and execution-failed states must be reported transparently and must not be silently dropped.

N.A. conditions: report `N.A.` when execution is outside the approved scope for the method or engine.

## Correctness Metrics

### Result Consistency Rate

Definition: fraction of selected/planned candidate cases whose observed result is exact/result-consistent under the checker or retained result-comparison protocol.

Formula:

`Result Consistency Rate = exact / selected`

Paper notation: `|X_r| / N_S`

Denominator: selected/planned candidate cases for the approved method and scope. Do not use an executed-candidate denominator for the canonical Result Consistency Rate.

Record types used: `rewrite_candidate_cell`; `control_cell` may support package/control reporting but is not a rewrite-method candidate denominator.

Eligibility:

- Candidate must be selected/planned in the approved denominator.
- Candidate must have an exact/result-consistent checker outcome to count in the numerator.
- Candidate execution failures, checker failures, missing candidates, unsupported/fail-closed rows, and mismatches remain denominator-visible non-numerator rows unless a later approved denominator policy says otherwise.
- Result consistency is an execution-evidence correctness metric; it does not by itself claim formal semantic proof.

Diagnostic boundary:

- An executed-subset consistency view may appear only as a separately named diagnostic, such as `executed_subset_consistency`.
- Executed-subset consistency must not replace the canonical Result Consistency Rate.
- Current `src/sql_rewrite_bench/local_metrics.py` behavior using `exact / selected` is the aligned D033 local diagnostic behavior.

N.A. conditions:

- Report `N.A.` only when no approved selected/planned denominator exists for the method/scope.

### Semantic Equivalence Rate

Definition: fraction of verifier-decidable exact/result-consistent candidate cases for which semantic equivalence is established by formal verifier evidence.

Formula:

`Semantic Equivalence Rate = |V_equiv| / |V_equiv union V_non|`

Denominator: decidable formal verifier outcomes over exact/result-consistent source-vs-candidate pairs: `equivalent + non_equivalent`.

Record types used: `rewrite_candidate_cell` with `verifier_support_pair` as support evidence.

Eligibility:

- Candidate must already be exact/result-consistent under the local checker or retained result-comparison protocol.
- Source-vs-candidate verifier pairs are constructed only for exact/result-consistent rows.
- SER is computed only from formal verifier evidence.
- Local result-checker exactness must not be used as SER evidence.
- Unknown, timeout, unsupported, `not_implemented`, `tool_error`, `no_verifier_support`, and `not_attempted` outcomes are excluded from the decidable SER denominator and reported separately.
- SQLSolver and VeriEQL are verifier/support tools, not rewrite baselines.
- Verifier outputs must remain separate from method-generated candidate failures and package hard-negative checker controls.
- Verifier limitations must not be counted as method rewrite failures.

SER status:

- Every route must report SER status as one of `computed`, `coverage_limited`, or `N.A.`.
- `computed`: formal verifier evidence exists and all approved eligible exact/result-consistent rows in the scope have decidable verifier outcomes.
- `coverage_limited`: formal verifier evidence exists for only a subset of approved eligible exact/result-consistent rows, or some attempted verifier outcomes are non-decidable and reported separately.
- `N.A.`: no approved formal verifier evidence exists for the route/scope.

N.A. conditions:

- Report `N.A.` when no approved formal verifier evidence exists for the route/scope.
- No official SER is produced by this contract patch.

## Performance Metrics

### GM Speedup Ratio

Definition: geometric mean speedup over strict exact/result-consistent timed candidate cases.

Formula:

`GM Speedup Ratio = geometric_mean(speedup_ratio for strict_exact_timed_rows)`

Denominator: strict exact + timed candidate cases.

Record types used: `rewrite_candidate_cell`.

Eligibility:

- Candidate must be exact/result-consistent.
- Candidate must have usable timing evidence.
- Timing must be eligible under the approved timing policy.
- Speedup must not be computed over incorrect, mismatch, execution-failed, unsupported, or timing-ineligible rows.
- Under the current strict-label policy, `label_only_mismatch` remains a mismatch and timing-ineligible unless a future policy changes it.
- Missing timing is not zero.

N.A. conditions:

- Report `N.A.` when no result-consistent timed cases exist for the method/scope.

### Speedup Ratio Percentiles

Definition: percentile summary of speedup ratios over strict exact/result-consistent timed candidate cases.

Formula:

Report P10, P25, P50, P75, and P90 over strict exact + timed speedup-ratio rows.

Denominator: strict exact + timed candidate cases.

Record types used: `rewrite_candidate_cell`.

Eligibility:

- Same as `GM Speedup Ratio`.
- Every percentile table should report the number of result-consistent timed cases.

N.A. conditions:

- Report `N.A.` when no result-consistent timed cases exist for the method/scope.

Legacy diagnostic:

- `Regression@20` is not part of formal local metrics v0.
- `Regression@20` may remain only as a legacy/reporting diagnostic if separately labeled and not mixed into formal local metrics v0.

## Interpretability Metrics

### Positive Operation Coverage Rate

Definition: paper-facing interpretability metric over externally defined positive operation atoms.

Formula:

`Positive Operation Coverage Rate = |C_r|^-1 sum_{i in C_r} (|A_hat_i| / |A_exp_i|)`

Denominator: operation-atom eligible cases with stable externally supplied expected operation atoms.

Record types used: future external collaborator operation-atom/skill-adapter evidence, only after a separately authorized integration task defines the schema.

Eligibility:

- POCR implementation is deferred to a separately authorized external collaborator script / operation-atom schema.
- Current local/public v0 metrics must report POCR as `N.A.` or deferred unless external operation-atom evidence exists.
- Do not create skill folders as part of this contract.
- Do not create operation atom files as part of this contract.
- Do not infer operation atoms from taxonomy tags, SQL text, `positive.sql`, manifest descriptions, README text, or checker files.
- Do not use `tag_slices` as POCR.
- Do not use failure buckets as POCR.
- Do not use plan deltas as POCR unless a future external operation-atom evidence contract explicitly authorizes it.

N.A. conditions:

- Report `N.A.` or deferred when external operation-atom evidence is absent or the POCR denominator is not defined.

Support boundary:

- Attribution Coverage is historical/superseded relative to the current paper-facing POCR name. It may appear only as support-context wording if separately labeled and must not replace POCR.
- Tag slices, failure buckets, and plan observability remain diagnostic/support evidence and must not replace POCR.
- Future POCR integration must be a separately authorized task after the collaborator's external operation-atom script/schema is stable.

## Generalization Metrics

### Cross-Engine Execution Coverage Rate

Definition: fraction of approved cross-engine candidate cases that execute on the target engine.

Formula:

`Cross-Engine Execution Coverage Rate = |E_tgt_r| / N_PORT`

Denominator: `N_PORT`, the approved cross-engine portability/generalization denominator. This is separate from Track A same-engine denominators.

Record types used: `portability_candidate_cell`.

N.A. conditions: report `N.A.` when a target engine or portability scope is unsupported or lacks an approved denominator.

### Cross-Engine Result Consistency Rate

Definition: fraction of approved cross-engine candidate cases that produce target-engine results consistent with the approved cross-engine checking protocol.

Formula:

`Cross-Engine Result Consistency Rate = |X_tgt_r| / N_PORT`

Denominator: `N_PORT`, the approved cross-engine portability/generalization denominator.

Record types used: `portability_candidate_cell`.

N.A. conditions: report `N.A.` when no approved cross-engine denominator exists for the scope.

### Cross-Engine GM Speedup Ratio

Definition: geometric mean speedup over target-engine strict exact/result-consistent timed candidate cases.

Formula:

`Cross-Engine GM Speedup Ratio = exp(|M_tgt_r|^-1 sum_{i in M_tgt_r} log s_tgt_i)`

Denominator: target-engine paired source/candidate timing rows that are exact/result-consistent in the same target-engine context.

Record types used: paired `portability_candidate_cell` rows.

Policy:

- Cross-Engine GM Speedup Ratio requires target-engine paired source/candidate timing in the same target-engine context.
- Track A same-engine timing must not be reused as Track C transfer-speed evidence.
- Speedup Retention is historical/superseded by the current paper-facing Cross-Engine GM Speedup Ratio wording.

N.A. conditions:

- Report `N.A.` when target-engine paired timing does not exist, is unsupported, or is outside the approved protocol.
- Missing paired timing is not zero and is not a cross-engine performance failure unless a later approved policy says so.

## Diagnostic And Support Fields

The following remain diagnostic/support unless a later approved contract promotes them:

- failure bucket distribution;
- tag_slices / retained-taxonomy slices;
- SQL extraction status;
- parseability;
- runnable SQL status;
- readiness/ready rate;
- unsupported status;
- preflight-blocked status;
- source-like/no-op status;
- PlanAvailability;
- PlanFrontier / plan observability summaries;
- atom-based Rewrite Opportunity Observability Score, unless and until the external POCR contract promotes explicit operation-atom evidence;
- verifier support counts outside Semantic Equivalence Rate.

Failure buckets are diagnostic only. `Candidate Failure Rate` is removed as a primary metric.

Failure bucket and tag-slice policy:

- Failure buckets are diagnostic/support only.
- `tag_slices` are diagnostic/support only.
- They are not primary metrics.
- They are not ranking scores.
- They are not leaderboard inputs.
- They must not replace POCR.
- They are useful for route boundary reporting, failure analysis, and taxonomy-aware diagnostic slices.

## Renamed, Removed, Or Demoted Metrics

| Older name | v1 status |
|---|---|
| Generatable Rate | renamed to Generation Rate |
| Exact Correctness Rate | renamed to Result Consistency Rate |
| Executed-denominator Result Consistency | superseded by canonical `exact / selected` |
| Speedup Distribution | renamed to Speedup Ratio Percentiles |
| Regression@20 | removed as primary; optional legacy diagnostic only |
| Candidate Failure Rate | removed as primary; failure buckets diagnostic only |
| Observability / PlanFrontier | support/diagnostic only; not POCR |
| Attribution Coverage | historical/superseded relative to current paper-facing POCR; support-context only if separately labeled |
| Speedup Retention | historical/superseded relative to current paper-facing Cross-Engine GM Speedup Ratio |
| Support Layer | removed as independent layer; verifier evidence folded into correctness |

Public table-column wording should prefer `Description` over `Interpretation`.

## Record Type Boundaries

- `rewrite_candidate_cell`: same-engine rewrite candidate metrics.
- `control_cell`: source/positive/hard-negative controls and checker guard evidence; not rewrite-method performance denominator rows.
- `portability_candidate_cell`: cross-engine/generalization metrics; not Track A same-engine rows.
- `plan_observability_artifact`: support/diagnostic explainability evidence.
- `verifier_support_pair`: correctness/semantic-equivalence support only.
- SQLSolver and VeriEQL outputs: verifier/support evidence only; not rewrite baselines and not method-generated candidate failures.
- `retained_summary_artifact`: traceability or comparison target, not a canonical metric row by default.
- `user_run_candidate_cell`: future user submissions after public runner policy is implemented.

## Implementation Status

Formalized metrics contract: yes, D032/D033 aligned.

Non-official local metrics implementation exists for local diagnostics only.

Official metrics implementation authorized: no.

Retained-evidence adapter implementation authorized: no.

POCR implementation authorized: no; deferred to external collaborator operation-atom/skill-adapter task.

Unified reproduction CLI implementation authorized: no.

Public runner implementation authorized: no.

Paper table rendering authorized: no.

Reports/results migration authorized: no.

Any future official implementation must first define adapter row materialization, validate denominator joins, preserve diagnostic states, and maintain no-global-leaderboard reporting.

## Local Vs Official Boundary

- `src/sql_rewrite_bench/local_metrics.py` outputs are non-official local diagnostic metrics.
- Local metrics must not update top-level `reports/`.
- Local metrics must not update top-level `results/`.
- Local metrics must not promote retained evidence.
- Local metrics must not render paper tables.
- Local metrics must not create a leaderboard.
- Denominator, case membership, paper results, retained evidence, and raw legacy evidence must not change as a side effect of local metrics.
