# Current Output Inventory

Current user-run execution writes under `runs/user/<run_id>/` through `src/sql_rewrite_bench/user_run.py`. Local metrics are currently produced by `scripts/dev/compute_local_user_metrics.py` into `runs/user/<run_id>/metrics/`.

## Current Files

| Current artifact | Writer | Future placement | Notes |
| --- | --- | --- | --- |
| `config.yaml` | `user_run.py` | source for `output/results/<run_id>/run_manifest.json` and `output/logs/<run_id>/command.log` | Current config is not the final manifest schema. |
| `selected_cases.csv` | `user_run.py` | `output/results/<run_id>/selected_cases.csv` or manifest support artifact | Useful for selection audit. |
| `ledger.csv` | `user_ledger.py` | `output/results/<run_id>/ledger.csv` | Row-grained status ledger. |
| `failures.csv` | `user_ledger.py` | source for `output/results/<run_id>/failure_buckets.csv` and `output/logs/<run_id>/failures.log` | Current file is row-level failure data, not a bucket summary. |
| `summary.json` | `user_run.py` | source for `output/reports/<run_id>/summary.md` | Current local summary remains useful but is not the final user-facing report. |
| `report.md` | `user_run.py` | source for `output/reports/<run_id>/summary.md` | Human-readable current run summary. |
| `quality_summary.json` | `user_quality_report.py` | `output/results/<run_id>/quality_summary.json` | Contains local-only boundary and funnel/failure diagnostics. |
| `quality_report.md` | `user_quality_report.py` | source for `output/reports/<run_id>/summary.md` | Human-readable quality report. |
| `tag_slices.csv` | `tag_slices.py` through `user_run.py` | `output/results/<run_id>/tag_slices.csv` | Needs paired `output/reports/<run_id>/tag_slices.md`. |
| `candidate_sql/` | adapter runner through `user_run.py` | `output/results/<run_id>/candidates/` | Candidate SQL artifacts. |
| `workspaces/` | adapter, execution, checker | split across `candidates/`, `execution/`, `checker/`, and logs | Needs implementation-time inventory by artifact type. |
| `timing/` | local timing helper through `user_run.py` | `output/results/<run_id>/timing/` | Existing v0 timing shape should be reused. |
| `metrics/` | `compute_local_user_metrics.py` | `output/results/<run_id>/metrics/` and `output/reports/<run_id>/metrics_summary.md` | Local-only, non-official metrics. |

## Current Command Surface

The current internal runner is:

```text
python -m sql_rewrite_bench.user_run
```

It already supports selection helpers through `--list-cases`, `--explain-selection`, and `--show-output-schema`, and local diagnostic execution through adapter, DB/checker, and timing flags. The future `sqlrb user ...` facade should delegate to this implementation rather than duplicating selection, execution, checking, timing, or metric logic.
