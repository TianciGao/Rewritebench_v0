# LearnedRewrite Fake Runtime User-Facade Smoke v0

## Summary

This packet records a no-runtime D035 user-facade smoke for the LearnedRewrite fake runtime adapter.

The smoke invoked:

```bash
python -m cli.main user evaluate
```

with `baselines/learnedrewrite/adapter.py`, fake runtime mode, PostgreSQL only, and two selected Common-core rows:

- `PERF_0006 / postgres`
- `CONS_0036 / postgres`

The facade selected 2 rows, generated 2 candidate SQL files, and wrote LearnedRewrite adapter metadata for both rows.

## Boundary

- Real LearnedRewrite Java runtime was not run.
- No Java server or JAR was invoked.
- No upstream source, JAR, dependency JAR, checkpoint, dataset, generated output, or request log was copied.
- No DB execution, checker execution, timing, local metrics, verifier, official metrics, paper rendering, retained-evidence promotion, leaderboard generation, or Track A 120 run occurred.
- Runtime artifacts stayed under ignored `runs/user/` and `/tmp`; they are not committed.

## Next Safe Action

Authorize a LearnedRewrite external-runtime availability/preflight audit. Do not run the real Java runtime on Common-core cases until external runtime path, request/response schema, extraction guards, and source-hygiene boundaries are verified.
