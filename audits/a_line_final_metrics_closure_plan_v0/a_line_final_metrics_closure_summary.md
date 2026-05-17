# A-line Final Metrics Closure Plan v0

## Purpose And Scope

This planning packet closes the current A-line state for existing experiment data, retained-evidence organization, and metric-readiness. It classifies all ten Metrics Contract v1 primary metrics and recommends the smallest remaining task sequence before moving to reproduction, user-runner, or broader case-universe lines.

No new metrics were computed. No official metrics were recomputed. No paper tables were rendered. No `reports/` or `results/` outputs were created or updated. Denominator values, paper results, case membership, and raw legacy evidence were unchanged.

## A-line Current State

- Common-core 40 canonical case packages are complete.
- `case_sets/common_core_v0/` and `inventory/` are aligned.
- Track A same-engine denominator scaffold remains 120 planned case-engine rows.
- Five Track A method routes produce 600 planned candidate rows in the candidate scaffold.
- Control scaffold remains 360 planned control rows.
- Retained evidence mapping and ledger mapping audits exist.
- Evidence ledger schema, row-grain policy, validator skeleton, fixture smoke, and CI smoke exist.
- Control-layer adapters and closeout are complete.
- Candidate-status evidence advanced from 600 unresolved rows to combined candidate status overlay v2 with 312 filled rows and 288 unresolved rows.
- Limited official status metrics v0 computed Execution Coverage Rate and Result Consistency Rate only.

## Already Official

- Execution Coverage Rate: official limited status metric available.
- Result Consistency Rate: official limited status metric available.

Both are denominator-aware and not paper results. Future rendering requires separate authorization and caveat handling.

## Audit-only Available

- Generation-related inferred evidence exists in audit-only status inference and dry-run artifacts.
- Status-only dry-run v4 exists and includes SQLGlot coverage context.
- Retained evidence maps and dependency matrices exist for future adapter planning.

Audit-only artifacts are not paper results and must not be copied into report outputs as official values.

## Blocked

- Generation Rate is blocked by `inferred_generated_policy_not_official_and_sqlglot_generated_ready_gap`.
- Semantic Equivalence Rate is blocked by missing verifier support adapter and decidability policy.
- GM_Speedup and Speedup Ratio Percentiles are blocked by missing timing adapter and timing eligibility.

## N.A. For v0

- Speedup Retention should be treated as N.A. for v0 because paired source/target result-consistent timing is unavailable and no portability timing protocol is implemented.

## Post-release Backlog

- Attribution Coverage should move to post-release attribution schema and evidence-pipeline work.
- Cross-Engine Execution and Cross-Engine Consistency should move to post-release portability adapter work unless the maintainer explicitly prioritizes a bounded portability packet before B-line.

## Recommended Remaining A-line Task Sequence

1. `generation_rate_blocker_final_decision`: decide whether Generation Rate remains blocked, becomes diagnostic-only, or receives a narrow observed-evidence completion task.
2. `non_status_metric_na_backlog_closure_bundle`: close Semantic Equivalence, performance, attribution, cross-engine, and Speedup Retention as blocked/N.A./post-release without implementing adapters.
3. `a_line_final_renderer_input_package`: package official limited status metrics plus blocked/N.A./post-release decisions for a future renderer without rendering.

## Exact Next Safe Action

Run `generation_rate_blocker_final_decision_v0` as a policy/evidence decision packet. It should compute no metrics, render no tables, write no reports/results, and decide the v0 treatment for Generation Rate before paper-facing renderer planning.
