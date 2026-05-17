# SQLGlot Candidate Status Parser v1 Limitations

- Audit-only parser output; not an official benchmark result.
- Only sanitized non-timing projection rows are used.
- Generated and ready are not inferred from checker-event artifact paths.
- Timing, latency, speedup, and timing eligibility fields remain blank or N.A.
- Rows without a case_id x engine x rewrite_method projection match remain unresolved.
- SQLGlot metric-input authorization is not created by this task.
