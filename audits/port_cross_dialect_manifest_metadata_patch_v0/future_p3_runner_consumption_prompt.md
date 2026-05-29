# Future P3 Runner Consumption Prompt

Task title:
P3 consume PORT local-diagnostic manifest role metadata in the user-entry runner

Purpose:
Update the user-entry resolver/runner/engine-router handoff to read the explicit `local_diagnostic` metadata added to the 9 Common-core PORT manifests and fail closed when a required backend or role is unavailable.

Allowed source modifications:

- `src/sql_rewrite_bench/case_package_resolver.py`
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/engine_execution.py`
- `src/sql_rewrite_bench/user_ledger.py`
- tests under `tests/user_entry/`
- static validator support for the additive `local_diagnostic` top-level key, if needed
- audit packet and project-control status/run-log updates

Do not authorize:

- SQL edits.
- Manifest edits beyond test fixtures unless separately approved.
- MySQL execution implementation.
- Spark execution implementation.
- Timing/speedup.
- Official metrics.
- Paper table rendering.
- Reports/results updates.
- Retained-evidence promotion.
- Global leaderboard.

Required behavior:

- Resolver reads and validates `local_diagnostic`.
- Same-engine cases preserve current PostgreSQL behavior.
- Cross-dialect cases identify MySQL source-reference requirements.
- While MySQL backend remains unavailable, cross-dialect cases fail closed with explicit local diagnostic status.
- Runner must not infer roles from file names, SQL text, or pool name.
- Runner must not silently use `pos_01.sql` as a source oracle.
- Runner must not silently fall back from MySQL or Spark to PostgreSQL.
- Ledger records metadata/backend fail-closed status locally.
- Reports/results and official metrics remain untouched.

Validation:

- Unit tests for same-engine metadata consumption.
- Unit tests for cross-dialect metadata fail-closed behavior with missing MySQL backend.
- Tests proving `pos_01.sql` is not used as source oracle.
- Static v2 validator accepts additive `local_diagnostic` metadata.
- Public smoke dry-run and adapter-capture behavior unchanged.
- Protected-surface check.
