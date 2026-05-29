# PORT Cross-Dialect Checker Normalization v0

Verdict: `completed_local_diagnostic_checker_change`.

This packet documents the implementation of a narrow opt-in checker normalization policy for manifest-declared PORT cross-dialect local diagnostics. The policy is enabled only when resolved manifest metadata has `local_diagnostic.diagnostic_mode == cross_dialect_reference` and `local_diagnostic.checker.comparison == source_reference_result_to_target_candidate_result`.

## Implemented Behavior

- Column-label positional comparison: implemented for opt-in cross-dialect rows after strict JSON object equality fails.
- Decimal string equivalence: implemented for opt-in cross-dialect rows using `Decimal` for numeric-looking string pairs.
- Same-engine default behavior: preserved.
- PERF, CONS, LONGTAIL, and same-engine PORT rows: not switched to positional comparison by default.

## Controlled Rerun

Run output path: `runs/user/port_pg_target_reference_normalized/`.

| Field | Count |
|---|---:|
| Selected rows | 5 |
| MySQL source-reference executable rows | 5 |
| PostgreSQL target-candidate executable rows | 5 |
| Checker attempted rows | 5 |
| Exact rows | 5 |
| Mismatch rows | 0 |

The four prior normalization-gap mismatches became exact. `PORT_0025` remained exact.

## Boundary

This is local diagnostic checker behavior only. No SQL files, manifests, schema files, checker configs, validation files, case sets, reports/results, denominators, paper results, case membership, raw retained evidence, timing/speedup, official metrics, or leaderboard outputs were changed.

## Next Safe Action

Review the opt-in checker details and controlled rerun artifacts. If accepted, keep the policy local-diagnostic only and do not use these exact rows as official metrics or paper results.
