# Run Scope

Scope was restricted to Common-core v0 PostgreSQL rows for:

- `method_id = calcite_hep_fail_closed`
- `route_id = calcite_hep_fail_closed`
- Engine: `postgres`
- Source audit: `audits/calcite_hep_pg_execution_checker_diagnostic_v0/`

The prior execution/checker audit supplied the exact gate:

- Selected rows: 40
- Generated candidate rows: 33
- No-candidate rows: 7
- Execution-attempted rows: 33
- Exact/result-consistent rows: 20
- Mismatch rows: 3
- Source execution failures: 2
- Candidate execution failures: 8

Timing was attempted only for rows where `exact = true` in `per_row_execution_checker_status.csv`.

The pass did not run MySQL, Spark, Direct LLM, Repair-1, SQLSolver, VeriEQL, full Common-core, all 120 Track-A rows, result checking, official metric computation, or paper result generation.
