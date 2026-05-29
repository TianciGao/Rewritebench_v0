# Spark Live Two-Case Smoke v0

Verdict: `completed`

## Summary

This packet records a bounded Spark live local diagnostic smoke for `common_core_v0` on `PERF_0006` and `CONS_0005` using `examples/user/noop_adapter.py`.

The accepted local run is `runs/user/spark_live_smoke/`. It selected 2 Spark rows, generated 2 candidates, passed candidate preflight for 2 rows, executed Spark source SQL for 2 rows, executed Spark candidate SQL for 2 rows, attempted the checker for 2 rows, and reached exact 2 with mismatch 0.

Failure bucket summary: `none=2`.

An initial sandboxed attempt reached runner completion but Spark failed to start because Py4J could not bind a local socket. That output was discarded and the same smoke was rerun with local socket access. The accepted run executed through PySpark and wrote source/candidate JSONL artifacts plus checker artifacts under each row workspace.

## Local-Only Boundary

This is local diagnostic evidence only. It is not official paper evidence, not retained evidence, not a metric input, not a paper table, and not a leaderboard.

No official metrics were computed. No timing or speedup was computed. No `reports/` or `results/` files were updated. No denominator, paper result, case membership, case package, SQL, schema, checker, validation, manifest, or raw retained evidence files were changed.

The local run output under `runs/user/spark_live_smoke/` is ignored local diagnostic output and is not committed.

## Recommended Next Safe Action

If Spark work continues, the next safe action is a separately authorized bounded Common-core Spark local diagnostic trial under the same local-only, non-metric, no timing, no reports/results, and no leaderboard boundaries.
