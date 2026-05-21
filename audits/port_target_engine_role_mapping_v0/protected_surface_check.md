# Protected Surface Check

Allowed changed files for this task:

- 9 PORT `manifest.yaml` files
- `src/sql_rewrite_bench/case_package_resolver.py`
- `src/sql_rewrite_bench/case_package_v2_resolver.py`
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/engine_execution.py`
- `src/sql_rewrite_bench/user_run_schema.py`
- tests under `tests/user_entry/` and `tests/case_package_v2/`
- `audits/port_target_engine_role_mapping_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces unchanged:

- SQL files: unchanged.
- Schema files: unchanged.
- Checker files: unchanged.
- Validation files: unchanged.
- `case_sets/`: unchanged.
- Reports/results: unchanged.
- Denominator scaffolds: unchanged.
- Paper results: unchanged.
- Case membership: unchanged.
- Raw legacy evidence: unchanged.
- Docs/examples/scripts outside validator/runtime support: unchanged.

Boundary confirmations:

- Official metrics computed: no.
- Timing/speedup computed: no.
- Reports/results updated: no.
- Global leaderboard created: no.
- Release tag/export branch created: no.
- Local `runs/user/` outputs are ignored local diagnostics and are not staged or committed.
