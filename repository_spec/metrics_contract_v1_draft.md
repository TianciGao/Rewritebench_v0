# Metrics Contract v1 Draft

Status: superseded by `repository_spec/metrics_contract_v1.md`

This draft has been formalized into `repository_spec/metrics_contract_v1.md`. Keep this file as historical alignment context only. The v1 contract is the current metric policy source; neither this draft nor the v1 contract authorizes metrics implementation, retained-evidence adapter implementation, paper table rendering, report/result migration, DB validation, denominator changes, paper-result changes, or case membership changes.

Purpose: define the public workbench metric contract direction after maintainer review of the updated paper metric scope.

This draft does not authorize metrics implementation, retained-evidence adapter implementation, unified reproduction CLI implementation, public runner implementation, paper table rendering, report/result migration, metric recomputation, denominator updates, paper result updates, case membership changes, or a global leaderboard.

Some metrics are approved in direction, but still require retained-evidence adapter coverage, ledger row-grain validation, and public reporting code before they can be computed or rendered.

## Updated Metric Suite

The updated draft metric suite is organized into five layers.

| Layer | Metric | Draft status | Primary row types |
|---|---|---|---|
| Coverage | Generation Rate | approved draft direction | `rewrite_candidate_cell`, future `user_run_candidate_cell` |
| Coverage | Execution Coverage Rate | approved draft direction | `rewrite_candidate_cell`, future `user_run_candidate_cell` |
| Correctness | Result Consistency Rate | approved draft direction | `rewrite_candidate_cell`, `control_cell` where applicable |
| Correctness | Semantic Equivalence Rate | approved draft direction, verifier-dependent | `rewrite_candidate_cell`, `verifier_support_pair` as support evidence |
| Performance | GM_Speedup | approved draft direction | exact and timed `rewrite_candidate_cell` rows |
| Performance | Speedup Ratio Percentiles | approved draft direction | exact and timed `rewrite_candidate_cell` rows |
| Explainability | Attribution Coverage | deferred implementation | `plan_observability_artifact` plus future attribution fields |
| Generalization | Cross-Engine Execution | approved draft direction | `portability_candidate_cell` |
| Generalization | Cross-Engine Consistency | approved draft direction | `portability_candidate_cell` |
| Generalization | Speedup Retention | approved draft direction, paired-timing dependent | paired exact and timed `portability_candidate_cell` rows |

## Coverage Metrics

### Generation Rate

Definition: fraction of planned candidate rows for which candidate SQL was generated.

Current meaning: candidate SQL generation only.

Boundary: extraction success, parser acceptance, execution readiness, and runnable SQL status are not second primary Generation Rate variants in this draft. They may remain diagnostic fields if later approved.

Required ledger fields:

- `record_type`
- `case_set`
- `denominator_id`
- `engine`
- `route`
- `method_role`
- `candidate_id`
- `candidate_sql_path`
- `generated`
- `result_status`

Denominator: approved candidate denominator for the route, such as Track A same-engine planned rows for same-engine rewrite metrics.

### Execution Coverage Rate

Definition: fraction of planned candidate rows that reached execution and have `executed=true` under the applicable route.

Boundary: execution coverage is not correctness. Unsupported, not-run, preflight-blocked, and missing-candidate states must be reported without being silently dropped.

Required ledger fields:

- `denominator_id`
- `engine`
- `route`
- `method_role`
- `executed`
- `result_status`
- `failure_stage`
- `failure_type`

## Correctness Metrics

### Result Consistency Rate

Definition: fraction of executed candidate rows whose observed result is consistent with the expected result under the checker or retained result comparison protocol.

Boundary: this metric is result-level consistency. It should not be used to imply formal semantic proof when only execution evidence is available.

Required ledger fields:

- `executed`
- `exact`
- `result_status`
- `checker_status`
- `retained_artifact_path`

Denominator: executed rows for the approved route unless a later contract explicitly selects planned rows.

### Semantic Equivalence Rate

Definition: fraction of candidates for which semantic equivalence is established by an approved semantic-equivalence basis.

Boundary: verifier evidence is incorporated into the correctness discussion for this metric. The previous independent Support Layer is removed. Verifier support is not a rewrite-generation baseline and does not create a separate leaderboard.

Required ledger fields:

- `exact`
- `checker_status`
- `evidence_source`
- `retained_artifact_path`
- verifier support evidence where available

Computability: depends on verifier decidability and available verifier/support evidence. Rows without applicable verifier support may be `N.A.` or reported under result consistency only, depending on the final adapter policy.

## Performance Metrics

### GM_Speedup

Definition: geometric mean speedup over exact and timed eligible rows.

Boundary: blank or missing timing is not zero. Performance interpretation is limited to rows with approved correctness and timing eligibility.

Required ledger fields:

- `exact`
- `timed`
- `latency_ms`
- `speedup`
- `timing_eligible`

Denominator: exact and timed eligible rows only.

### Speedup Ratio Percentiles

Definition: percentile summary of speedup ratios over exact and timed eligible rows.

Recommended fields include P25, median/P50, P75, and optional IQR or additional approved percentiles.

Boundary: this replaces or demotes Regression@20 as the primary performance-regression framing. Regression@20 may remain only as a diagnostic or legacy comparator if later needed for continuity.

Required ledger fields:

- `exact`
- `timed`
- `latency_ms`
- `speedup`
- `timing_eligible`
- grouping keys for case, engine, route, and method role

## Explainability Metrics

### Attribution Coverage

Definition: fraction of eligible rows or artifacts with sufficient retained attribution evidence to explain the rewrite decision, plan/failure observation, or comparison basis under a future attribution schema.

Draft boundary: Attribution Coverage is an updated paper-scope metric direction, but implementation is deferred because the exact attribution schema and eligible denominator are not finalized.

It must not overclaim internal optimizer reasoning. It should describe retained external-observable evidence such as public-safe plan artifacts, failure-stage attribution, checker evidence, verifier evidence used in correctness discussion, and curated explanation artifacts when available.

Required future fields may include:

- `plan_available`
- `plan_artifact_path`
- `failure_stage`
- `failure_type`
- `checker_status`
- `evidence_source`
- future attribution fields not yet added to the ledger schema

## Generalization Metrics

### Cross-Engine Execution

Definition: fraction of approved portability rows that execute on the target engine under the cross-engine route.

Boundary: this uses portability denominator semantics and must not be mixed with Track A same-engine rows.

### Cross-Engine Consistency

Definition: fraction of executed portability rows that produce consistent results on the target engine under the approved cross-engine checking protocol.

Boundary: this is separate from same-engine Result Consistency Rate.

### Speedup Retention

Definition: retained speedup ratio across source/target engine or source/target route pairs when both sides have exact and timed eligible evidence.

Computability: `N.A.` when paired target-engine timing is not supported or not available. Missing paired timing must not be treated as zero or failure.

Required ledger fields:

- source/target pairing keys;
- `exact`
- `timed`
- `latency_ms`
- `speedup`
- `timing_eligible`
- route and engine fields for both sides, either directly or through adapter join keys.

## Removed Or Demoted Primary Metrics

Candidate Failure Rate is removed as a primary metric. Failure buckets remain diagnostic and should support debugging, coverage interpretation, and report transparency.

Regression@20 is not a primary metric in the updated contract. It may remain as a diagnostic or legacy comparator only if the maintainer/team later requests it.

Extraction/readiness variants are not second primary Generation Rate definitions in this draft. Parseability, extractability, runnable SQL, ready/not-ready, unsupported, and preflight-blocked status may remain diagnostic ledger fields.

PlanFrontier and broad observability wording are replaced by the explainability-layer framing of Attribution Coverage. Plan and failure observability remain evidence inputs, not independent primary performance or correctness metrics.

Support Layer is removed as an independent layer. Verifier support is incorporated into correctness, especially Semantic Equivalence Rate, and remains non-baseline support evidence.

## Denominator Handling

The metrics contract preserves:

- Common-core v0 = 40 cases;
- Track A same-engine planned rows = 120;
- engines = PostgreSQL, MySQL, and Spark;
- no global leaderboard;
- role-aware denominator slices;
- control rows separate from candidate rows;
- portability rows separate from same-engine Track A rows;
- support/verifier rows separate from rewrite-generation baselines.

Each reported metric must state:

- denominator set;
- included rows;
- excluded rows;
- route and record-type scope;
- generation, execution, correctness, and timing gates where applicable;
- `N.A.` conditions.

## Implementation Gate

Before implementing retained-evidence adapters, metrics computation, a report renderer, unified reproduction CLI, or public runner:

- maintainer/team must approve this aligned draft or a successor final contract;
- retained-evidence adapters must map rows to the approved ledger record types;
- denominator joins must be validated against `case_sets/common_core_v0/`;
- Attribution Coverage denominator and attribution fields must be specified before implementation;
- Speedup Retention must define paired target-engine timing support before implementation;
- paper table rendering must remain unauthorized until explicitly approved.

This draft records aligned metric direction only.
