# User-Entry Local Quality Report v0

## Purpose

This packet records U4 local quality report v0 for the user-entry diagnostic path.

The implementation writes `quality_summary.json` and `quality_report.md` under each `runs/user/{run_name}/` output root. These files summarize the current user-run `ledger.csv` funnel and failure buckets for local diagnostics only.

## Implementation Summary

- Added `src/sql_rewrite_bench/user_quality_report.py`.
- Integrated local quality output generation into `src/sql_rewrite_bench/user_run.py` after `ledger.csv`, `failures.csv`, `summary.json`, and `report.md` are written.
- Added tests under `tests/user_entry/test_quality_report.py`.
- Preserved existing user-run outputs and smoke behavior.

## Boundary

- Local quality report is local diagnostic only.
- Official metrics computed: no.
- Paper tables rendered: no.
- Reports/results updated: no.
- Retained evidence parsed or promoted: no.
- Tag slices created: no.
- Timing or speedup computed: no.
- Live DB/checker execution run: no.
- Global leaderboard created: no.

## Verdict

U4 local quality report v0 is complete for the current user-entry local diagnostic path.

## Next Safe Action

Human review of `quality_summary.json` and `quality_report.md`; if accepted, authorize U5 tag-aware slices v0 as a separate local-diagnostic task.
