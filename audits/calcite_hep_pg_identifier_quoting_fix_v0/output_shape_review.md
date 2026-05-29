# Output Shape Review

Committed audit outputs:

- `target_rows.csv`
- `before_after_status.csv`
- `targeted_validation_summary.json`
- Markdown review files in this audit packet
- Audit helper `run_targeted_quote_validation.py`

Runtime outputs were written only under:

- `/tmp/sqlrb_calcite_hep_pg_identifier_quoting_fix_v0/output/results/calcite_hep_pg_identifier_quoting_fix/`
- `/tmp/sqlrb_calcite_hep_pg_identifier_quoting_fix_v0/output/logs/calcite_hep_pg_identifier_quoting_fix/`
- `/tmp/sqlrb_calcite_hep_pg_identifier_quoting_fix_v0/output/reports/calcite_hep_pg_identifier_quoting_fix/`

This follows the D035 local-output shape under a temporary root. No runtime outputs were committed.

The committed CSVs preserve row-level denominator visibility and include `local_only=true`, `official_metric_input=false`, and `paper_result=false`.
