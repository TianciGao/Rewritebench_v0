# Run Scope

Case set:

- `common_core_v0`

Planned rows:

- 40 Common-core cases
- engines: `postgres`, `mysql`, `spark`
- total planned rows: 120

Enabled:

- candidate generation / capture
- fail-closed handling
- source execution where applicable
- candidate execution where applicable
- local result checker where both source and candidate executed

Disabled:

- timing
- `compute-local-metrics`
- SQLSolver / VeriEQL
- SQLGlot / LLM baselines
- official metrics
- official Semantic Equivalence Rate
- formal Regression@20
- POCR
- paper reports/results
- retained evidence promotion
- leaderboard output

Runtime output root:

`/tmp/sqlrb_calcite_hep_track_a_120_execution_checker_diagnostic_v0/`
