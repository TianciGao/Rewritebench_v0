# LearnedRewrite Next Implementation Plan

## Phase 1: Fixture-Only Adapter Scaffold

Create `baselines/learnedrewrite/adapter.py` with fake mode only.

Required behavior:

- read D035 row environment;
- resolve source SQL and schema context;
- parse `SQLRB_LEARNEDREWRITE_FAKE_RESPONSE` as JSON;
- extract exactly one `rewritten_sql`;
- write candidate SQL only on success;
- write status metadata with local-only boundary flags;
- fail closed for missing schema, unsupported engine, malformed output, empty SQL, and multiple statements.

No Java, HTTP, DB, checker, timing, local metrics, verifier, or paper output.

## Phase 2: Fake External Runtime Tests

Add tests for the fixture matrix in `learnedrewrite_fixture_io_examples.csv`.

Minimum fixture coverage:

- complete JSON output;
- source-like/no-op candidate metadata;
- missing `rewritten_sql`;
- empty `rewritten_sql`;
- multiple SQL statements;
- invalid JSON;
- missing schema context;
- PostgreSQL eligible row;
- MySQL unsupported boundary;
- Spark unsupported boundary;
- timeout status simulation;
- metadata redaction.

## Phase 3: No-Runtime User-Facade Smoke

Run a tiny D035 user-facade smoke in fake mode over 1-2 rows.

Allowed only after Phase 1 and tests pass.

Expected checks:

- candidate SQL emitted for PostgreSQL fixture rows;
- unsupported boundaries remain no-candidate for MySQL/Spark if selected;
- metadata includes `route_id=learnedrewrite` and `method_id=learnedrewrite`;
- no Java runtime, DB, checker, timing, local metrics, verifier, or paper output.

## Phase 4: Bounded External-Runtime Smoke

Only if an external LearnedRewrite runtime is installed outside this repo and source/license hygiene is acceptable:

- use PostgreSQL only;
- run 1-3 rows;
- use a temp output root;
- do not compute aggregate metrics;
- do not update reports/results;
- record external runtime availability without copying binaries.

Abort if the runtime writes unsafe paths, emits ambiguous SQL, or cannot consume the schema JSON fixture.

## Phase 5: Track A Feasibility Decision

Track A 120 is realistic only if:

- the wrapper can select all 120 planned rows;
- unsupported engine rows remain visible;
- final row ledger is D035-shaped;
- DB/checker/timing behavior is stable where authorized;
- local metrics come only from `python -m cli.main user compute-local-metrics`;
- no paper or retained-evidence promotion is implied.

If MySQL/Spark remain unsupported, prefer bounded PostgreSQL appendix evidence rather than a misleading full 120 claim.
