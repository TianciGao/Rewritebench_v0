# LearnedRewrite External Wrapper

Status: adapter scaffold with fixture fake mode and gated HTTP runtime mode.
Command mode remains a fail-closed future hook.

Planned route identity:

- `route_id = learnedrewrite`
- `method_id = learnedrewrite`

LearnedRewrite must be integrated as an external tool wrapper. This repository must not vendor upstream LearnedRewrite source code, `rewriter_java.jar`, Calcite dependency JARs, checkpoints, datasets, generated outputs, request logs, or legacy runtime artifacts.

Adapter path:

```text
baselines/learnedrewrite/adapter.py
```

The adapter reads the standard D035 user-facade row environment, parses a fake
fixture response or a gated HTTP runtime response, and writes exactly one complete SQL candidate to
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

HTTP runtime mode:

```bash
SQLRB_LEARNEDREWRITE_MODE=http \
SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME=1 \
SQLRB_LEARNEDREWRITE_URL='http://127.0.0.1:6336/rewriter' \
python baselines/learnedrewrite/adapter.py
```

HTTP mode assumes the external LearnedRewrite server is already running outside
this repository. For the recovered JAR, stage required runtime assets such as
`rules_for_selected/` in a temporary workdir outside the release repo and start
the external JAR from that workdir. The adapter does not start Java and does not
copy runtime assets.

The HTTP request sends:

- `sql`: source SQL with comments stripped and terminal semicolon normalized;
- `schema`: a JSON-array string derived from PostgreSQL DDL or supplied through
  `SQLRB_LEARNEDREWRITE_SCHEMA_JSON`.

The HTTP response must contain `status=true` and `data.rewritten_sql`.

DB execution, checker execution, timing, local metrics, verifier use, and Track
A 120 are separate explicit authorizations.

Boundary:

- local diagnostic only;
- not an original-paper reproduction;
- not retained evidence promotion;
- not official metrics;
- not leaderboard input.
- no upstream source or JAR vendored.
