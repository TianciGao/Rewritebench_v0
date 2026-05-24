# LearnedRewrite External Wrapper

Status: design scaffold only. No adapter is implemented in this directory yet.

Planned route identity:

- `route_id = learnedrewrite`
- `method_id = learnedrewrite`

LearnedRewrite must be integrated as an external tool wrapper. This repository must not vendor upstream LearnedRewrite source code, `rewriter_java.jar`, Calcite dependency JARs, checkpoints, datasets, generated outputs, request logs, or legacy runtime artifacts.

The future adapter target is:

```text
baselines/learnedrewrite/adapter.py
```

The future adapter should read the standard D035 user-facade row environment, call either a fake fixture response or an externally supplied LearnedRewrite runtime, and write exactly one complete SQL candidate to `SQLRB_CANDIDATE_SQL_PATH` only when extraction is unambiguous.

Suggested future environment variables:

- `SQLRB_LEARNEDREWRITE_MODE`: `fake`, `http`, or `cmd`.
- `SQLRB_LEARNEDREWRITE_URL`: external HTTP `/rewriter` endpoint.
- `SQLRB_LEARNEDREWRITE_CMD`: external row-scoped wrapper command.
- `SQLRB_LEARNEDREWRITE_TIMEOUT`: per-row timeout.
- `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME`: required gate for real external runtime calls.
- `SQLRB_LEARNEDREWRITE_FAKE_RESPONSE`: fixture-only fake JSON response.

Initial implementation should be fixture-only and no-runtime. Real Java execution, DB execution, checker execution, timing, local metrics, verifier use, and Track A 120 are separate future authorizations.

Boundary:

- local diagnostic only;
- not an original-paper reproduction;
- not retained evidence promotion;
- not official metrics;
- not leaderboard input.
