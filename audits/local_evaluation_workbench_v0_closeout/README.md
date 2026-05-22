# Local Evaluation Workbench v0 Closeout

Verdict: `closed_for_local_evaluation_workbench_v0`

This audit-only closeout records the completed local evaluation workbench v0 surface. It covers user-entry local diagnostics, tri-engine local execution, checker/failure explanations, strict-label diagnostics, exact-gated local timing, and non-official local metrics projection.

No new feature was implemented. No Common-core rerun was performed. No new timing was collected. No official metrics, reports/results, retained-evidence promotion, paper table rendering, or leaderboard output was produced.

## Completed Workbench Surface

- User-entry adapter invocation and candidate capture are implemented through `sql_rewrite_bench.user_run`.
- Candidate preflight, local DB execution, checker handoff, ledger/failure-bucket outputs, quality summaries, and tag slices are available for local diagnostic runs.
- PostgreSQL, MySQL, and Spark local diagnostic backends are live for the supported local diagnostic roles.
- PORT controlled target-reference paths are separated from real adapter rows and explicit unsupported/fail-closed rows.
- Strict result-column label policy is documented, and label-only mismatch diagnostics are visible without changing exact/mismatch semantics.
- Exact-gated local timing is implemented as opt-in local diagnostic infrastructure, with bounded SQLGlot noop timing smoke over `PERF_0006` and `CONS_0005` on PostgreSQL, MySQL, and Spark.
- A non-official local metrics calculator is implemented and has projected local diagnostic metrics over existing Common-core SQLGlot noop snapshots.

## Current SQLGlot Noop Common-core Projection

| Engine | selected | generated | candidate executable | exact | mismatch | Generation Rate | Execution Coverage Rate | Result Consistency Rate | performance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| PostgreSQL | 40 | 35 | 35 | 35 | 0 | 0.875 | 0.875 | 0.875 | N.A., no timing artifacts |
| MySQL | 40 | 40 | 39 | 31 | 8 | 1.0 | 0.975 | 0.775 | N.A., no timing artifacts |
| Spark | 40 | 40 | 33 | 31 | 2 | 1.0 | 0.825 | 0.775 | N.A., no timing artifacts |

These are local diagnostic projections only. They are not official SQLGlot baseline evidence and not paper results.

## Deferred Scope

- Official metrics computation remains deferred.
- Retained-evidence promotion remains deferred.
- Paper table rendering remains deferred.
- Reports/results migration remains deferred.
- POCR and skill-adapter integration remain deferred pending the external operation-atom script and schema.
- Any exactness-changing label policy remains deferred and must be separately authorized.
- Broader local timing or official timing evidence promotion remains deferred.

## Next Safe Action

Use this closeout as the local evaluation workbench v0 stopping point. The next safe task is to choose between a bounded post-label-diagnostics refresh, timing hardening, retained-evidence/official promotion design, or pausing the local evaluation line before public-release packaging.
