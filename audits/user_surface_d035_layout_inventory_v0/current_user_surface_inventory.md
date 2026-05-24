# Current User Surface Inventory

User-facing CLI facade:

- `src/cli/__init__.py`
- `src/cli/__main__.py`
- `src/cli/main.py`

Core implementation package:

- `src/sql_rewrite_bench/adapter_runner.py`
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/user_output.py`
- `src/sql_rewrite_bench/user_ledger.py`
- `src/sql_rewrite_bench/user_quality_report.py`
- `src/sql_rewrite_bench/user_output_schema.py`
- `src/sql_rewrite_bench/local_metrics.py`
- `src/sql_rewrite_bench/local_timing.py`
- engine and checker helpers under `src/sql_rewrite_bench/`
- verifier support under `src/sql_rewrite_bench/verifier_support/`

Baseline adapters:

- `baselines/sqlglot/sqlglot_user_adapter.py`
- `baselines/sqlglot/README.md`
- `baselines/calcite_hep_fail_closed/adapter.py`
- `baselines/calcite_hep_fail_closed/README.md`

User examples:

- `examples/user/noop_adapter.py`
- `examples/user/port_mysql_target_reference_adapter.py`
- `examples/user/port_postgres_target_reference_adapter.py`
- `examples/user/port_spark_target_reference_adapter.py`

Documentation:

- root-level docs under `docs/*.md`
- development docs under `docs/dev/*.md`
- `docs/guide/`, `docs/spec/`, and `docs/templates/` are not present yet.

Development scripts:

- current development and validation tools remain under `scripts/dev/`.
- D035 target is `src/dev/`, but physical migration is explicitly deferred.

Tests:

- focused user-entry tests live under `tests/user_entry/`.
- these tests cover CLI facade behavior, output shape, user-run staging, SQLGlot adapter behavior, Calcite route behavior, verifier wrappers, local timing, local metrics, and engine execution routing.
