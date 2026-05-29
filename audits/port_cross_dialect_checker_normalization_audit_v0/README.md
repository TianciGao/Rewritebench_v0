# PORT Cross-Dialect Checker Normalization Audit

Verdict: `normalization_policy_gap`.

This audit inspected the controlled PostgreSQL-target diagnostic artifacts for five PORT cross-dialect rows: `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.

## Local Run Status

- Controlled diagnostic artifacts available: yes.
- Rerun required: no.
- PostgreSQL probe result: ok.
- MySQL probe result: ok.
- Spark status: deferred/fail-closed.
- MySQL source-reference execution succeeded for all five rows.
- PostgreSQL target-candidate execution succeeded for all five rows.
- Checker ran for all five rows.
- Exact rows: 1 (`PORT_0025`).
- Mismatch rows: 4 (`PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`).

## Mismatch Summary

The four mismatches do not show source-side, target-side, schema, connection, or checker-runtime failures. Each mismatch has one source row and one target row, with one output column on each side.

- `PORT_0004`: value `50` matches after ignoring the single output column label. The mismatch is caused by MySQL expression-derived column labeling versus PostgreSQL `?column?` labeling.
- `PORT_0013`: value `66.66666666666667` matches after ignoring the single output column label. The mismatch is caused by column-label comparison.
- `PORT_0022`: values are numerically equal (`0.25` versus `0.25000000000000000000`) after ignoring the output label. The mismatch combines column-label comparison and decimal-string formatting.
- `PORT_0024`: values are numerically equal (`50` versus `50.0000000000000000`) after ignoring the output label. The mismatch combines column-label comparison and decimal-string formatting.

`PORT_0025` reached exact because both engines emitted the same column label, `account_id`, and the same value, `2`.

## Interpretation Boundary

This is local diagnostic triage only. It is not official metrics, not paper reproduction, not timing or speedup, not a reports/results update, not retained evidence promotion, and not a leaderboard input. The audit did not modify checker behavior, SQL files, manifests, case files, schemas, checker configs, validation files, source code, or case-set membership.

## Recommended Next Safe Action

Authorize a narrow future checker-normalization task that adds an explicit cross-dialect comparison policy, with tests proving existing PERF, CONS, and LONGTAIL same-engine checker behavior is unchanged. Do not infer this policy from filenames, and do not compute metrics, timing, reports/results, or leaderboard outputs.
