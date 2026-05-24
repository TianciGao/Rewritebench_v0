# Multi-Engine Gap Review

Before this task:

- `user evaluate --engines postgres,mysql,spark` produced per-engine source runs.
- `user compute-local-metrics` accepted only `--run-id`, so it computed one source run at a time.
- There was no canonical user-facing command to combine `<run_id>__postgres`, `<run_id>__mysql`, and `<run_id>__spark` into a single Track A local diagnostic metrics output.
- Prior route cards therefore used audit-helper projections instead of canonical `local_metrics.py` outputs.

Gap found: yes.

Implemented correction:

- Added canonical aggregate functions in `src/sql_rewrite_bench/local_metrics.py`.
- Added aggregate CLI mode to `python -m cli.main user compute-local-metrics`.
- Kept formulas centralized in `local_metrics.py`; the CLI delegates only.

Combined Track A behavior:

- `selected_rows` are summed across source runs.
- `candidate_generated`, `candidate_executable`, and `exact` counts are summed across source runs.
- Timing rows are concatenated only when they are strict exact + timed rows.
- GM speedup and P10/P25/P50/P75/P90 are computed over the combined exact-timed speedup set by the canonical local metrics code.
