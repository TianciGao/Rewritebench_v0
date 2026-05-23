# Local Metric Interpretation

This task produced a local diagnostic verifier-support ledger only.

Computed local diagnostic values:

- `equivalent_count=4`
- `non_equivalent_count=1`
- `decidable_count=5`
- `local_bound4_pg_noop_semantic_equivalence_rate=0.8`
- `verifier_decidability_rate=0.14285714285714285`
- `verifier_decidable_coverage_over_exact_rows=0.14285714285714285`
- `verifier_attempt_coverage_over_exact_rows=1.0`

Interpretation:

- The local diagnostic rate is computed only over decidable VeriEQL outcomes.
- It excludes timeout, unsupported, not-implemented, syntax-error, unknown, out-of-memory, tool-error, and not-attempted rows.
- It is not official Semantic Equivalence Rate.
- It must not be promoted into paper tables or official reports/results.

The low decidable coverage means the rate alone would be misleading. Any future paper-facing metric would need to report verifier coverage and decidability alongside the rate.
