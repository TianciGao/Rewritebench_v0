# Output Path Review

The reviewed CLI remains aligned with D035:

- Result root: `output/results/<run_id>/`
- Log root: `output/logs/<run_id>/`
- Report root: `output/reports/<run_id>/`

`evaluate` uses `runs/user/<run_id>/` for the internal local diagnostic run, then delegates export to `sql_rewrite_bench.user_output.export_run_to_output`.

Hardening added in this task:

- `evaluate` validates the resolved output root with `build_output_paths(...)` before invoking the internal runner.
- `compute-local-metrics` validates the resolved output root before invoking the local metrics calculator.

This prevents accidental work before rejecting protected roots such as top-level `reports/` or `results/`.

Protected-surface tests confirm:

- `--output-root reports` is rejected before `run_user_benchmark`.
- `--output-root results` is rejected before `compute_and_write_local_metrics`.
- No top-level `reports/` or `results/` files were modified.
