# Reclassified Metric Interpretation

Corrected local diagnostic counts:

- Corrected equivalent rows: 4
- Corrected non-equivalent rows: 0
- Corrected decidable rows: 4
- Identity-failed rows: 31
- Not-attempted ineligible rows: 5

Corrected local diagnostic rate:

- `corrected_local_bound4_pg_noop_semantic_equivalence_rate=1.0`
- This is computed over 4 corrected decidable rows only.

Coverage:

- `corrected_verifier_decidability_rate=4/35 = 0.11428571428571428`
- `identity_pass_rate=4/35 = 0.11428571428571428`

Identity-passing rows:

- `CONS_0036`
- `CONS_0037`
- `PORT_0003`
- `PORT_0005`

Interpretation:

- All previously equivalent rows passed identity sanity.
- The only prior non-equivalent row, `LONGTAIL_0023`, failed identity sanity and is excluded from corrected `V_non`.
- The corrected local diagnostic SER is computable but coverage-limited.
- This rate is not official Semantic Equivalence Rate, not paper evidence, and not retained evidence.
