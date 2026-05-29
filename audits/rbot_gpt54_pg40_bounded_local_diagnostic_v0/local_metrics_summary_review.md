# Local Metrics Summary Review

The requested `python -m cli.main user compute-local-metrics` command was attempted after the PostgreSQL-only evaluate run.

Result: no `local_metrics.py` outputs were produced.

Blocker:

```text
error: aggregate_run_dir contains non-aggregate artifacts that could be exported as stale output: candidate_sql, failures.csv, quality_report.md, quality_summary.json, report.md, tag_slices.csv, timing, workspaces
```

Because local metrics did not produce output files, the following canonical local metric fields are not copied and are not hand-computed in this packet:

| field | value |
|---|---|
| selected | not produced by `local_metrics.py` |
| generated | not produced by `local_metrics.py` |
| candidate_executable | not produced by `local_metrics.py` |
| exact | not produced by `local_metrics.py` |
| mismatch | not produced by `local_metrics.py` |
| timed exact rows | not produced by `local_metrics.py` |
| generation rate | not produced by `local_metrics.py` |
| execution coverage | not produced by `local_metrics.py` |
| result consistency | not produced by `local_metrics.py` |
| GM speedup | not produced by `local_metrics.py` |
| P10/P25/P50/P75/P90 | not produced by `local_metrics.py` |
| SER status | not produced by `local_metrics.py`; no verifier was run |
| POCR status | not produced by `local_metrics.py`; POCR remains deferred/N.A. |

The evaluate ledger counts are summarized separately in `bounded_diagnostic_summary.json` and `bounded_diagnostic_report.md` as local diagnostic run facts, not canonical local metric outputs.
