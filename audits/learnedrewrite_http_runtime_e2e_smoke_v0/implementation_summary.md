# Implementation Summary

Files changed:

- `baselines/learnedrewrite/adapter.py`
- `baselines/learnedrewrite/README.md`
- `tests/user_entry/test_learnedrewrite_adapter.py`

Adapter behavior added:

- HTTP runtime mode is enabled only when `SQLRB_LEARNEDREWRITE_URL` is set and
  `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME=1`.
- The adapter sends `POST` JSON to the configured `/rewriter` endpoint.
- The request body contains `sql` and `schema`.
- The response must contain `status=true` and `data.rewritten_sql`.
- Candidate extraction still accepts exactly one SQL statement.
- HTTP mode fails closed on missing allow gate, missing URL, `status=false`,
  missing `data.rewritten_sql`, empty output, malformed JSON, timeout,
  connection error, unsupported engine, and ambiguous/multiple SQL.
- Fake runtime mode remains supported.
- Command mode remains a fail-closed future hook.

Schema behavior added:

- PostgreSQL DDL is converted into the LearnedRewrite schema JSON-array shape.
- DDL parser support is intentionally narrow: CREATE TABLE bodies, column names,
  common type normalization, and table-level constraint skipping.
- No case/schema files are mutated.

Runtime boundary:

- The adapter does not start Java.
- The external JAR and `rules_for_selected/` remain outside the release repo.
- Runtime staging was done only under `/tmp`.
