# Implementation Summary

Phase 2B adds a public facade package under `src/cli` and a console-script entry point:

- `src/cli/__init__.py`
- `src/cli/__main__.py`
- `src/cli/main.py`
- `pyproject.toml` entry point: `sqlrb = "cli.main:main"`

The facade is intentionally thin. It parses user-facing commands, translates arguments into existing internal interfaces, and delegates:

- Evaluation delegates to `sql_rewrite_bench.user_run.run_user_benchmark`.
- Output export delegates to `sql_rewrite_bench.user_output.export_run_to_output`.
- Case listing and selection explanation delegate to `sql_rewrite_bench.user_run.main`.
- Output schema display delegates to `sql_rewrite_bench.user_output_schema.output_schema_text`.
- Optional local metrics command delegates to `sql_rewrite_bench.local_metrics.compute_and_write_local_metrics`.

No rewrite logic, DB execution logic, checker logic, verifier logic, metrics formulas, or output-contract business rules are duplicated in `src/cli`.

The `evaluate` command preserves `runs/user/<run_id>/` as the internal local diagnostic run root and exports the user-facing surface to:

- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

Relative output roots are resolved against the repository root. For multiple engines, the facade creates per-engine run ids using `<run_id>__<engine>` to avoid route/output mixing.

Verifier flags are accepted only as reserved values and fail closed with a clear error because VeriEQL and SQLSolver integration is not implemented in Phase 2B.
