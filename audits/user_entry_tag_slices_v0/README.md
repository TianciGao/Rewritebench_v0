# User-Entry Tag-Aware Slices v0

## Purpose

This packet records U5 tag-aware diagnostic slices for the user-entry path.

The implementation writes `tag_slices.csv` under each `runs/user/{run_name}/`
output root. The file joins local user-run ledger rows with retained
case-package taxonomy metadata and reports denominator-aware local diagnostic
counts by tag.

## Implementation Summary

- Added `src/sql_rewrite_bench/tag_slices.py`.
- Integrated `tag_slices.csv` generation into `src/sql_rewrite_bench/user_run.py`
  after local quality report generation.
- Updated `src/sql_rewrite_bench/user_quality_report.py` so the local quality
  boundary records that tag slices are available.
- Added tests under `tests/user_entry/test_tag_slices.py`.

## Tag Source

Tags are loaded from retained `manifest.yaml` taxonomy metadata through the
already resolved case package. Tags are not inferred from SQL text, pool name,
runtime behavior, retained evidence, reports, or results.

## Boundary

- Tag slices are local diagnostic only.
- No tag score was created.
- No ranking was created.
- Official metrics computed: no.
- Paper tables rendered: no.
- Reports/results updated: no.
- Retained evidence parsed or promoted: no.
- Timing or speedup computed: no.
- Live DB/checker execution run: no.
- Global leaderboard created: no.

## Verdict

U5 tag-aware diagnostic slices v0 are complete for the current user-entry local
diagnostic path.

## Next Safe Action

Human review of `tag_slices.csv`; if accepted, authorize U6 user readability
enhancements or defer to the next approved user-entry phase.
