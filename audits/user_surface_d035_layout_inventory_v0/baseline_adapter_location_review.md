# Baseline Adapter Location Review

Baseline-specific adapter files currently live under `baselines/`.

SQLGlot:

- `baselines/sqlglot/sqlglot_user_adapter.py`
- `baselines/sqlglot/README.md`

Calcite HEP fail-closed:

- `baselines/calcite_hep_fail_closed/adapter.py`
- `baselines/calcite_hep_fail_closed/README.md`

Core source review:

- No tracked `src/sql_rewrite_bench/calcite_hep_fail_closed_adapter.py` exists.
- No tracked SQLGlot adapter implementation exists under `src/sql_rewrite_bench/`.
- `src/sql_rewrite_bench/adapter_runner.py` is generic adapter invocation infrastructure and correctly remains core.

Verifier distinction:

- `src/sql_rewrite_bench/verifier_support/sqlsolver.py` and `verieql.py` are verifier-support wrappers, not rewrite baselines.
- They correctly remain under `src/sql_rewrite_bench/verifier_support/`.

Verdict:

- Baseline adapter locations are D035-compliant.
- No adapter move is recommended in this task.
