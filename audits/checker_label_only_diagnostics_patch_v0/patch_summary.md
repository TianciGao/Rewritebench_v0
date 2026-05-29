# Patch Summary

## Code Changes

- `src/sql_rewrite_bench/local_result_checker.py`
  - Computes strict label/value diagnostics after existing normalization.
  - Emits label-only mismatch details while preserving strict checker outcomes.
  - Writes `label_diagnostics` into mismatch artifacts.
  - Adds a checker note marker for downstream local diagnostic summaries.

- `src/sql_rewrite_bench/user_quality_report.py`
  - Adds `diagnostic_counts.label_only_mismatch_rows` to `quality_summary.json`.
  - Adds a `Diagnostic classifications` section to `quality_report.md`.

## Behavior Preservation

Existing exact/mismatch semantics are unchanged:

- Labels and values match: remains exact.
- Values match but labels differ: remains mismatch, now marked `label_only_mismatch=true`.
- Values differ: remains mismatch, marked `value_exact=false`.
- Row count, column count, row order, or multiplicity differences are not classified as label-only.
- Explicit alias differences remain strict mismatch.
- Generated-expression label differences are diagnostic-only and are not converted to exact.
- Existing manifest-gated cross-dialect comparison remains separate from same-engine strict label diagnostics.

## Non-Changes

- No checker policy was relaxed.
- No SQLGlot adapter behavior changed.
- No case-local checker config was added.
- No global label-ignore behavior was introduced.
- No official metrics, timing/speedup, reports/results, paper outputs, retained evidence, or leaderboard were produced.
