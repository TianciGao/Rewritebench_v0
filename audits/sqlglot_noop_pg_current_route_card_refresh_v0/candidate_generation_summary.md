# Candidate Generation Summary

SQLGlot noop candidate generation used:

- adapter: `baselines/sqlglot/sqlglot_user_adapter.py`
- adapter route: `--route noop`
- selected rows: 40
- generated candidates: 35
- no-candidate rows: 5
- candidate origin for generated rows: `sqlglot_noop`

The five no-candidate rows failed closed during SQLGlot parsing:

| case_id | pool | status | likely cause |
| --- | --- | --- | --- |
| PORT_0004 | PORT | adapter_failed | cross-dialect MySQL-like PORT source SQL parsed as PostgreSQL |
| PORT_0013 | PORT | adapter_failed | cross-dialect MySQL-like PORT source SQL parsed as PostgreSQL |
| PORT_0022 | PORT | adapter_failed | cross-dialect MySQL-like PORT source SQL parsed as PostgreSQL |
| PORT_0024 | PORT | adapter_failed | cross-dialect MySQL-like PORT source SQL parsed as PostgreSQL |
| PORT_0025 | PORT | adapter_failed | cross-dialect MySQL-like PORT source SQL parsed as PostgreSQL |

The representative raw adapter failure was a SQLGlot parse error on MySQL-style backtick quoting in a PostgreSQL route. The rows were recorded as local diagnostic no-candidate rows rather than being dropped.
