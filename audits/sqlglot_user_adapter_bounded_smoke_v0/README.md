# SQLGlot User-Adapter Bounded Smoke v0

Verdict: `completed_with_failures`

This packet records a bounded local diagnostic smoke for the existing SQLGlot user-entry adapter routes:

- `python baselines/sqlglot/sqlglot_user_adapter.py --route noop`
- `python baselines/sqlglot/sqlglot_user_adapter.py --route optimize`

SQLGlot was available locally as version `30.2.1`; no package installation was required.

## Route Summary

`sqlglot_noop`:
- Phase A PostgreSQL adapter-capture run selected 2 rows and generated 2 candidates with DB/checker disabled.
- Phase B same-engine bounded DB/checker smoke passed on PostgreSQL, MySQL, and Spark: each engine selected 2 rows, generated 2 candidates, executed 2 source rows, executed 2 candidate rows, attempted 2 checker rows, and reached exact `2/2`.
- Phase C PORT probe was run only for the no-op route because its Phase B same-engine smoke passed. The PostgreSQL target probe on `PORT_0004` failed at adapter parse time before candidate generation. The MySQL target probe on `PORT_0003` generated and executed a candidate but produced a checker mismatch.

`sqlglot_optimize`:
- Phase A PostgreSQL adapter-capture run selected 2 rows and generated 2 candidates with DB/checker disabled.
- Phase B same-engine bounded DB/checker smoke completed with candidate execution failures on `CONS_0005` for PostgreSQL, MySQL, and Spark. `PERF_0006` was exact on all three engines. The failing optimized candidate referenced `table1.table2.i`, which each engine rejected as an unresolved/unknown column path.
- Phase C PORT probe was skipped for the optimize route because Phase B did not fully succeed.

## Interpretation

These are local diagnostic adapter rows, not official SQLGlot baseline evidence. `sqlglot_noop` and `sqlglot_optimize` are separate routes and are not merged into one SQLGlot score.

The PORT rows in this packet are real SQLGlot adapter behavior only. They are not controlled target-reference diagnostics and are kept separate from the closed PORT controlled paths.

## Boundary

- Local diagnostic only.
- Official metrics computed: no.
- Timing or speedup computed: no.
- Reports/results updated: no.
- Paper results changed: no.
- Denominator changed: no.
- Case membership changed: no.
- Raw retained evidence changed: no.
- Retained evidence promoted: no.
- Leaderboard created: no.
- Release/export/tag created: no.
- `runs/user/` outputs committed: no.

## Recommended Next Safe Action

Triage `sqlglot_optimize` on `CONS_0005` as an adapter route behavior issue before any broader optimize-route trial. Keep any PORT real-adapter probes separate from controlled target-reference diagnostics and continue to avoid timing, official metrics, reports/results, retained evidence, and leaderboard outputs.
