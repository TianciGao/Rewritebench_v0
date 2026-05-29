# Local Metric Display Policy

Allowed local diagnostic display:

- `corrected_local_bound4_pg_noop_semantic_equivalence_rate=1.0`
- denominator: 4 corrected decidable rows
- coverage: 4/35 exact rows
- policy: `finite_bound_bound4_timeout30_cores1`

Required adjacent fields:

- selected rows
- exact candidate rows
- source-vs-candidate attempted rows
- identity-checked rows
- identity-passed rows
- identity-failed rows
- corrected equivalent count
- corrected non-equivalent count
- corrected decidable count
- unsupported, timeout, not-implemented, and tool-error counts

Forbidden display:

- Do not call the corrected local diagnostic rate official Semantic Equivalence Rate.
- Do not display it without coverage.
- Do not place it in top-level `reports/` or `results/`.
- Do not use it as paper evidence.
- Do not combine it with rows from another bound policy.
