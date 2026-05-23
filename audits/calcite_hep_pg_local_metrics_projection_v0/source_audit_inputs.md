# Source Audit Inputs

This projection aggregates only already-produced local diagnostic audit outputs.

Candidate generation input:

- Audit: `audits/calcite_hep_pg_bounded_candidate_generation_v0/`
- Summary file: `diagnostic_summary.json`
- Per-row file: `per_row_candidate_status.csv`
- Selected rows: 40
- Generated candidate rows: 33
- No-candidate rows: 7

Execution/checker input:

- Audit: `audits/calcite_hep_pg_execution_checker_diagnostic_v0/`
- Summary file: `diagnostic_summary.json`
- Per-row file: `per_row_execution_checker_status.csv`
- Execution-attempted rows: 33
- Source-executable rows: 31
- Candidate-executable rows: 23
- Checker-attempted rows: 23
- Exact/result-consistent rows: 20

Timing input:

- Audit: `audits/calcite_hep_pg_exact_timing_diagnostic_v0/`
- Summary file: `diagnostic_summary.json`
- Per-row file: `per_row_timing.csv`
- Exact timed rows: 20
- Timing failures: 0
- Diagnostic GM speedup: 0.995749

The projection did not read or depend on uncommitted runtime output as metric input.
