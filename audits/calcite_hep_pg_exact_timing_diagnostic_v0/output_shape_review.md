# Output Shape Review

Runtime timing artifacts were written only under:

- `/tmp/sqlrb_calcite_hep_pg_exact_timing_diagnostic_v0/output/results/calcite_hep_pg_exact_timing/`
- `/tmp/sqlrb_calcite_hep_pg_exact_timing_diagnostic_v0/output/logs/calcite_hep_pg_exact_timing/`
- `/tmp/sqlrb_calcite_hep_pg_exact_timing_diagnostic_v0/output/reports/calcite_hep_pg_exact_timing/`

Committed audit outputs are limited to:

- `per_row_timing.csv`
- `diagnostic_summary.json`
- Markdown review files
- The audit-local helper script

No repository-level `output/`, `runs/user/`, top-level `reports/`, or top-level `results/` runtime artifacts are part of this audit packet.
