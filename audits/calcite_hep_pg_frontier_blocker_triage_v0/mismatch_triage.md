# Mismatch Triage

Mismatch rows: 3.

Rows:

- `PERF_0035`
- `PERF_0062`
- `CONS_0011`

Source audit notes:

- `PERF_0035` and `PERF_0062` are column-count/shape mismatches in the local checker output.
- `CONS_0011` is a label-only mismatch under the strict local checker; values match but labels differ by case.

Classification:

- Primary category: `calcite_generated_candidate_semantic_mismatch`
- Secondary category: `manual_review_required`
- Safe next action: `manual_case_review`

These rows should not be timed, promoted, or interpreted as exact until manually reviewed and, if appropriate, rerun after a specific candidate-generation or checker-label policy fix.
