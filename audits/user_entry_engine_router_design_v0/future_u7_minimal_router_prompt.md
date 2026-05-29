# Future Prompt: U7 Minimal Engine Router Implementation

Task title:
U7 minimal implementation of user-entry engine execution router and fail-closed MySQL/Spark interfaces

Purpose:
Implement the minimal behavior-preserving router designed in `audits/user_entry_engine_router_design_v0/`.

Allowed implementation:

- Add `src/sql_rewrite_bench/engine_execution.py` as a router/dispatcher.
- Add fail-closed `src/sql_rewrite_bench/mysql_execution.py` stub.
- Add fail-closed `src/sql_rewrite_bench/spark_execution.py` stub.
- Modify `src/sql_rewrite_bench/user_run.py` only to call the router instead of importing PostgreSQL execution directly.
- Preserve current PostgreSQL local diagnostic behavior.
- Add tests for router dispatch, PostgreSQL preservation, MySQL fail-closed behavior, Spark fail-closed behavior, and no silent fallback.

Do not implement:

- live MySQL execution
- live Spark execution
- timing diagnostics
- speedup
- official metrics
- paper table rendering
- retained-evidence parsing
- reports/results updates
- full paper reproduction CLI
- global leaderboard

Validation:

- `git diff --check`
- Python compile for changed modules
- module help
- wrapper help
- public smoke dry-run
- public smoke adapter-capture
- mocked router tests
- `PYTHONPATH=src pytest tests/user_entry`
- protected-surface check confirming no changes to cases, case_sets, reports, results, denominator scaffolds, paper results, or raw retained evidence

Boundary:

User-run outputs remain local diagnostics under `runs/user/{run_name}/`. No official metrics, paper tables, reports/results, retained evidence, timing/speedup, denominator changes, case membership changes, or leaderboard output are authorized.
