# non_official_local_metrics_calculator_v0

Verdict: `completed`

This task implements a non-official local metrics calculator for user-run local diagnostic outputs, following D033.

The calculator reads `runs/user/{run_name}/` artifacts and writes local-only metrics under `runs/user/{run_name}/metrics/`. It does not compute official metrics, update `reports/` or `results/`, promote retained evidence, render paper tables, implement POCR, create skill folders, or create leaderboard output.

## Implementation

- Added `src/sql_rewrite_bench/local_metrics.py`.
- Added `scripts/dev/compute_local_user_metrics.py`.
- Added focused tests in `tests/user_entry/test_local_metrics.py`.

## Implemented Local Metrics

- Generation Rate: `candidate_generated / selected`.
- Execution Coverage Rate: `candidate_executable / selected`.
- Result Consistency Rate: `exact / selected`.
- GM Speedup Ratio over strict exact + timed rows only.
- Speedup Ratio Percentiles P10, P25, P50, P75, P90 over strict exact + timed rows only.

## Deferred / N.A.

- Regression@20 is not implemented.
- Semantic Equivalence Rate is `N.A.` without formal verifier evidence.
- Cross-Engine GM Speedup Ratio is `N.A.` without target-engine paired timing.
- POCR is deferred with `skill_adapter_pending=true`.

## Bounded Smoke

The calculator was run against the existing bounded SQLGlot noop timing smoke artifacts:

- `runs/user/timing_sqlglot_noop_postgres_smoke/`
- `runs/user/timing_sqlglot_noop_mysql_smoke/`
- `runs/user/timing_sqlglot_noop_spark_smoke/`

Each run selected 2 rows, generated 2 candidates, had 2 candidate-executable rows, 2 exact rows, and 2 exact timed rows. Local metrics outputs were written under each run's ignored `metrics/` directory and were not committed.

## Metadata Correction

The prior `local_metrics_v0_final_formula_decision_v0` run-log entry still recorded commit/push as pending. This task records that final commit `2990340ec5a0d4682288e125606caf85d146d558` was pushed to `origin/feature/case-package-v2-external-schema`.
