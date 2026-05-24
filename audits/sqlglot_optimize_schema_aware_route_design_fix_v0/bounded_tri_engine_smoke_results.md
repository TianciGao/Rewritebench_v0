# Bounded Tri-Engine Smoke Results

Smoke scope:
- Cases: `CONS_0005`, `PERF_0006`, `CONS_0036`
- Engines: `postgres`, `mysql`, `spark`
- Route: `sqlglot_optimize_schema_aware`
- Runtime root: `/tmp/sqlrb_sqlglot_optimize_schema_aware_route_design_fix_v0/`

Results:
- Rows attempted: 9
- Candidate generated rows: 9
- Adapter return code 0 rows: 9
- Candidate preflight passed rows: 9
- Prior invalid `CONS_0005` qualification rows: 0

Not run:
- DB execution
- local result checker
- timing
- SQLSolver
- VeriEQL
- full Track A 120

Artifacts committed in this audit:
- `per_row_smoke_status.csv`
- `diagnostic_summary.json`

Interpretation:
- The immediate `CONS_0005` invalid qualification blocker is addressed for bounded generation/preflight.
- The route still needs a bounded tri-engine execution/checker diagnostic before being treated as ready for a larger Track A local diagnostic run.
