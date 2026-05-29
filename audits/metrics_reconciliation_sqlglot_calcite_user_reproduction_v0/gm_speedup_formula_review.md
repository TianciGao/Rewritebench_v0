# GM Speedup Formula Review

The local metrics artifacts define GM Speedup Ratio as `geometric_mean(speedup_ratio)` over strict exact+timed rows. The per-row timing CSVs record `speedup_ratio`, `source_median_ms`, and `candidate_median_ms`. Per-row timing JSON confirms the intended direction: `speedup_ratio = source_median_ms / candidate_median_ms` when both medians are present.

Rows with missing timing, timeout, zero, non-exact status, execution failure, unsupported status, or no candidate are excluded because `included_in_performance=false`. This task did not change formulas.

## SQLGlot no-op

- Prior timed rows: 97
- New timed rows: 97
- Prior-only timed rows: 0
- New-only timed rows: 0
- Common timed rows: 97
- Common timed rows with identical speedup: 0
- Common timed rows with different speedup: 97

Finding: The exact+timed row set is identical, but every common timed row has a different speedup value. The cause is fresh source/candidate runtime measurement provenance, with canonical timing using 5 measured repetitions and the new nightly reproduction using 2 measured repetitions.

## SQLGlot optimize schema-aware

- Prior timed rows: 66
- New timed rows: 66
- Prior-only timed rows: 0
- New-only timed rows: 0
- Common timed rows: 66
- Common timed rows with identical speedup: 0
- Common timed rows with different speedup: 66

Finding: The exact+timed row set is identical, but every common timed row has a different speedup value. The cause is fresh source/candidate runtime measurement provenance, with canonical timing using 5 measured repetitions and the new nightly reproduction using 2 measured repetitions.

## Calcite HEP fail-closed

- Prior timed rows: 80
- New timed rows: 0
- Prior-only timed rows: 80
- New-only timed rows: 0
- Common timed rows: 0
- Common timed rows with identical speedup: 0
- Common timed rows with different speedup: 0

Finding: The new run has no exact+timed rows because Calcite runtime was missing, so GM is N.A.; this is a blocked-runtime environment difference, not a formula change.

Conclusion: GM discrepancies for SQLGlot are not caused by formula direction or exact/timed eligibility. They are caused by fresh timing measurements and timing policy/provenance differences. Calcite is blocked by missing runtime env.
