# Implementation Summary

Files changed:

- `src/sql_rewrite_bench/local_metrics.py`
- `src/cli/main.py`
- `tests/user_entry/test_local_metrics.py`
- `tests/user_entry/test_cli_facade.py`

Core metrics changes:

- Added `compute_aggregate_local_metrics(...)`.
- Added `compute_and_write_aggregate_local_metrics(...)`.
- Refactored single-run metrics through shared enriched-row and write helpers.
- Added summary `aggregation_policy` metadata showing source run ids, source run paths, denominator combination, timing combination, and local-only boundary.
- Added a minimal aggregate source-run writer so D035 export can copy canonical aggregate `metrics/` outputs without changing `user_output.py`.

CLI changes:

- `user compute-local-metrics --run-id` remains the single-run path.
- `user compute-local-metrics --run-id-prefix --engines --aggregate-run-id` is the multi-engine aggregate path.
- Aggregate mode validates complete options and rejects mixing `--run-id` with aggregate options.

No route-specific metric logic was added to baseline adapters or audit helpers.
