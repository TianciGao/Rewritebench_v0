# Validation Notes

Validation scope:

- Markdown non-empty checks for all generated packet files.
- Source audit existence checks for:
  - `audits/learnedrewrite_pg40_bounded_local_diagnostic_v0/`
  - `audits/learnedrewrite_http_runtime_e2e_smoke_v0/`
  - `audits/learnedrewrite_temp_runtime_staging_preflight_v0/`
  - `audits/prior_methods_onboarding_feasibility_v0/`
- Copied PG40 metric value checks against `audits/learnedrewrite_pg40_bounded_local_diagnostic_v0/bounded_diagnostic_summary.json` and `local_metrics_summary_review.md`.
- CSV/JSON parse checks: no new CSV or JSON files are created by this policy packet; existing source audit JSON/CSV files were read as source evidence.
- No-prohibited-command check: command log contains read-only inspection and validation only.
- `git diff --check`: planned/passed before closeout.
- Changed-file secret scan: planned/passed before closeout.
- Protected-path review: planned/passed before closeout.

Copied PG40 values checked:

- selected: 40
- generated: 29
- candidate executable: 23
- exact: 17
- timed exact rows: 17
- mismatch: 6
- candidate_execution_failed: 6
- fail-closed/no-candidate: 11
- Generation Rate: 0.725
- Execution Coverage: 0.575
- Result Consistency: 0.425
- GM speedup: 1.0291029729677286
- P10/P25/P50/P75/P90: 0.8134186116858578 / 0.9784093859740545 / 1.0023559404279565 / 1.014471169398659 / 1.704766251233957

Boundary result:

- no new experiment run
- no runtime command run
- no `compute-local-metrics` command run
- no top-level reports/results update
- no retained evidence promotion
- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
