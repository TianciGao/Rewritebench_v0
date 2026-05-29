# Spark Backend Test Plan

## Mocked Unit Tests

- Spark environment detector returns `spark_not_configured` when explicit local Spark opt-in is absent.
- Spark environment detector returns `spark_client_missing` when `pyspark` cannot be imported.
- Spark schema resolver reads only `engines.spark.ddl` and `engines.spark.load` from the external schema profile.
- Spark schema resolver fails closed when `engines.spark` is absent.
- Spark schema resolver fails closed when Spark DDL/load paths are missing.
- Spark resolver never substitutes PostgreSQL or MySQL schema assets for Spark.
- Spark execution result maps Spark-specific failures to existing failure buckets without adding official metric fields.
- Spark result JSONL export preserves column labels and column order for simple fake rows.
- Spark result JSONL export serializes decimals, dates, timestamps, booleans, and NULLs according to the documented policy.
- `local_result_checker.py` can consume fake Spark same-engine source/candidate JSONL artifacts.

## Router and Ledger Tests

- `--engine spark` same-engine non-PORT rows dispatch to Spark backend when implemented, or to fail-closed Spark skeleton before implementation.
- PORT rows with `engine_roles.spark.diagnostic_mode=unsupported` fail closed and do not infer roles.
- Missing Spark target role fails closed.
- PostgreSQL same-engine behavior remains unchanged.
- MySQL same-engine behavior remains unchanged.
- Existing PORT MySQL/PostgreSQL bidirectional controlled routes remain unchanged.
- Quality summary and tag slices tolerate Spark fail-closed statuses.
- No timing/speedup fields are introduced.
- No reports/results are written.

## Optional Live Spark Smoke

Only after mocked tests pass and a separate task authorizes live execution:

- Start with 1-2 simple same-engine cases with existing Spark DDL/load assets, for example `PERF_0006` and `CONS_0005`.
- Use the no-op adapter.
- Run under `runs/user/<run_name>/` only.
- Record exact/mismatch as local diagnostics only.
- Do not run all 40 cases until the smoke passes and runtime is known to be safe.

## No-Spark CI Behavior

CI should not require live Spark. Without Spark, tests should assert deterministic fail-closed statuses and avoid importing or starting Spark unless explicitly mocked.

## Protected-Surface Checks

Every implementation phase must confirm no changes to source SQL, manifests unless specifically authorized, schema/checker/validation files, case_sets, reports/results, denominators, paper results, case membership, raw evidence, timing outputs, or leaderboard outputs.
