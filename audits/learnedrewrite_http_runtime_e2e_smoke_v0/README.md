# LearnedRewrite HTTP Runtime E2E Smoke

This packet records a narrow LearnedRewrite external-runtime user-facade smoke.
The adapter HTTP mode was implemented in `baselines/learnedrewrite/adapter.py`,
then the D035 user facade was run over one PostgreSQL Common-core row with DB
execution, checker, and timing enabled.

Selected row:

- `CONS_0036 / postgres`

`PERF_0006` was not included in this first external-runtime smoke because the
runtime has not yet been validated on TPC-H date/comment-heavy SQL. The selected
row has the same PostgreSQL, schema-JSON, and single-query characteristics used
to validate the synthetic runtime preflight, while still exercising the user
facade, DB execution, checker, and timing path.

Result summary:

- selected rows: 1
- candidates generated: 1
- candidate executable rows: 1
- exact rows: 1
- timed rows: 1
- fail-closed rows: 0

No Track A 120 run, `compute-local-metrics`, verifier, official metrics, paper
rendering, retained-evidence promotion, or leaderboard output occurred.

Next safe action: authorize a 5-10 row PostgreSQL-only LearnedRewrite bounded
diagnostic with DB/checker/timing. Do not run Track A 120 until that bounded
diagnostic passes.
