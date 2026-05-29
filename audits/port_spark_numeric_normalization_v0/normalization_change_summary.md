# Normalization Change Summary

The checker change is intentionally narrow:

- Existing cross-dialect positional comparison remains gated by resolved manifest local diagnostic metadata.
- New mixed numeric equivalence is a second opt-in, enabled only by the runner for resolved MySQL-source to Spark-target diagnostics.
- Safe decimal parsing accepts strings and JSON numeric values only when both are finite and decimal-equivalent.
- Booleans are explicitly excluded even though Python booleans are integer subclasses.
- Nulls, arbitrary strings, identifiers, dates, NaN, and infinity are not coerced.

Implementation details:

- `src/sql_rewrite_bench/local_result_checker.py` adds `_safe_decimal`, `_mixed_numeric_equal`, and an `enable_mixed_numeric_equivalence` argument to `run_local_checker`.
- `src/sql_rewrite_bench/user_run.py` derives the opt-in from resolved manifest metadata through `_mysql_to_spark_numeric_equivalence_enabled`.
- The existing `enable_cross_dialect_normalization` boolean remains unchanged for PostgreSQL/MySQL cross-dialect positional comparison.

No checker YAML or case manifest changes were made.
