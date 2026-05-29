# PostgreSQL Noop Verifier Coverage Summary

Source run:

- `runs/user/common_core_pg_noop_db_checker`

Source-run counts:

- Selected rows: 40
- Exact/result-consistent rows: 35
- Non-exact verifier-ineligible rows: 5

Raw source-vs-candidate VeriEQL outcomes under `finite_bound_bound4_timeout30_cores1`:

- `equivalent`: 4
- `non_equivalent`: 1
- `timeout`: 8
- `unsupported`: 16
- `not_implemented`: 5
- `tool_error`: 1
- `not_attempted_ineligible`: 5

After identity guard:

- Corrected equivalent rows: 4
- Corrected non-equivalent rows: 0
- Corrected decidable rows: 4
- Identity-failed exact rows: 31

Coverage:

- Corrected decidable coverage over exact rows: 4/35
- Identity pass rate: 4/35

The corrected local diagnostic rate is numerically 1.0, but the coverage is too low for paper-facing interpretation.
