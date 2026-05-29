# Local Metric Interpretation

The diagnostic summary reports:

- `corrected_local_sqlsolver_pg_noop_semantic_equivalence_rate = 1.0`
- `corrected_decidable_count = 24`
- `corrected_equivalent_count = 24`
- `corrected_non_equivalent_count = 0`
- `corrected_sqlsolver_decidable_coverage_over_exact_rows = 24/35`

This is a local diagnostic support metric over corrected SQLSolver-decidable rows only. It is not official Semantic Equivalence Rate and is not paper output.

Excluded from corrected decidable rows:

- unknown identity rows;
- timeout identity rows;
- not-attempted ineligible rows;
- any future tool-error, unsupported, syntax-error, not-implemented, or OOM rows.

Local result-checker exactness was not used as verifier evidence.
