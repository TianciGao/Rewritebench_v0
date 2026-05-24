# LearnedRewrite External Wrapper

Status: fixture-only adapter scaffold. The adapter supports fake runtime mode
only; command and HTTP modes are present as fail-closed future hooks.

Planned route identity:

- `route_id = learnedrewrite`
- `method_id = learnedrewrite`

LearnedRewrite must be integrated as an external tool wrapper. This repository must not vendor upstream LearnedRewrite source code, `rewriter_java.jar`, Calcite dependency JARs, checkpoints, datasets, generated outputs, request logs, or legacy runtime artifacts.

Adapter path:

```text
baselines/learnedrewrite/adapter.py
```

The adapter reads the standard D035 user-facade row environment, parses a fake
fixture response, and writes exactly one complete SQL candidate to
`SQLRB_CANDIDATE_SQL_PATH` only when extraction is unambiguous. Expected
fail-closed cases exit with code 0 and write `learnedrewrite_status.json` under
`SQLRB_WORKSPACE_DIR` without writing candidate SQL.

Suggested future environment variables:

- `SQLRB_LEARNEDREWRITE_MODE`: `fake`, `http`, `cmd`, or `command`.
- `SQLRB_LEARNEDREWRITE_URL`: external HTTP `/rewriter` endpoint.
- `SQLRB_LEARNEDREWRITE_CMD`: external row-scoped wrapper command.
- `SQLRB_LEARNEDREWRITE_TIMEOUT`: per-row timeout.
- `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME`: required gate for real external runtime calls.
- `SQLRB_LEARNEDREWRITE_FAKE_RESPONSE`: fixture-only fake JSON response.
- `SQLRB_LEARNEDREWRITE_FAKE_SQL`: fixture-only inline SQL response.
- `SQLRB_LEARNEDREWRITE_SCHEMA_JSON`: optional fixture-only inline schema JSON marker.

Fake response examples:

```bash
SQLRB_LEARNEDREWRITE_MODE=fake \
SQLRB_LEARNEDREWRITE_FAKE_RESPONSE='{"status":"ok","rewritten_sql":"SELECT 1 AS ok"}' \
python baselines/learnedrewrite/adapter.py
```

```bash
SQLRB_LEARNEDREWRITE_MODE=fake \
SQLRB_LEARNEDREWRITE_FAKE_SQL='SELECT 1 AS ok' \
python baselines/learnedrewrite/adapter.py
```

This implementation is fixture-only and no-runtime. Real Java execution, DB
execution, checker execution, timing, local metrics, verifier use, and Track A
120 are separate future authorizations.

Boundary:

- local diagnostic only;
- not an original-paper reproduction;
- not retained evidence promotion;
- not official metrics;
- not leaderboard input.
- no upstream source or JAR vendored.
