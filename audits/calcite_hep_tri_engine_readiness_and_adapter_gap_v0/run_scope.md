# Run Scope

Route:

- `route_id = calcite_hep_fail_closed`
- `method_id = calcite_hep_fail_closed`
- adapter: `baselines/calcite_hep_fail_closed/adapter.py`

Engines:

- `postgres`
- `mysql`
- `spark`

Bounded matrix:

| case_id | pool | reason |
|---|---:|---|
| `PERF_0006` | PERF | Known Calcite candidate-generation success row. |
| `CONS_0005` | CONS | Join/qualification control row. |
| `CONS_0036` | CONS | Prior label-only mismatch and quoting frontier row. |
| `CONS_0037` | CONS | Prior exact row after PostgreSQL quoting fix. |
| `PORT_0004` | PORT | DATETIME/TIMESTAMP style no-candidate blocker row. |
| `PORT_0024` | PORT | PORT source-role / cross-dialect reference row. |

Planned rows: 18 = 6 cases x 3 engines.

Enabled:

- candidate generation / capture
- source DB execution where a candidate exists and the runner can execute it
- candidate DB execution where a candidate exists
- local checker where source and candidate execution both succeed

Disabled:

- full Track A 120
- timing
- SQLSolver / VeriEQL
- `compute-local-metrics`
- official metrics
- paper reports/results
- retained evidence promotion
- leaderboard output
