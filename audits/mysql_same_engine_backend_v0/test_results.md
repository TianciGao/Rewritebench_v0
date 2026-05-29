# Test Results

Validation performed:

- `git diff --check`: passed after audit packet creation.
- Python compile for modified source files: passed.
- Environment check: PostgreSQL ok, MySQL ok, Spark deferred/fail-closed.
- Help commands: module help and wrapper help passed.
- Readability commands: `--list-cases`, MySQL smoke `--explain-selection`, and `--show-output-schema` passed.
- Public PostgreSQL smoke dry-run and adapter-capture commands passed.
- Targeted MySQL/router/checker regression tests: 31 passed.
- Full user-entry tests: 102 passed, 2 skipped using the existing `/tmp/sqlrb_pytest_venv` environment.
- Common-core v2 static case-package reference validation: passed for all 40 case paths.
- MySQL same-engine live smoke: passed for `PERF_0006` and `CONS_0005`.
- PORT cross-dialect controlled regression: passed exact 5/5.
- Audit CSV/JSON/Markdown sanity checks: passed.
- Protected-surface diff check: passed; only allowed code, test, audit, and project-control files changed.

The repository environment did not expose a bare `pytest` command on `PATH`, so tests were run with the existing local test environment by prefixing `PATH=/tmp/sqlrb_pytest_venv/bin:$PATH`. Live MySQL was not required for CI-style tests; mocked tests cover fail-closed behavior.

No timing/speedup, official metrics, reports/results updates, retained-evidence promotion, or leaderboard outputs were produced.
