# Semantic Equivalence Summary Review

The SQLSolver wrapper reuses `generate_semantic_equivalence_summary`.

Policy:

- `decidable_count = equivalent_count + non_equivalent_count`.
- `semantic_equivalence_rate = equivalent_count / decidable_count` only when `decidable_count > 0`.
- If SQLSolver is unavailable or no decidable verifier outputs exist, `semantic_equivalence_rate=null` and `na_reason` is explicit.
- Unknown, timeout, unsupported, tool-error, and not-attempted rows remain separately counted and excluded from the rate denominator.
- Local result-checker exactness is not used as verifier evidence.

Observed fail-closed smoke:

- `decidable_count=0`
- `semantic_equivalence_rate=null`
- `na_reason=sqlsolver_unavailable`
- `not_attempted_count=1`

This is a local diagnostic summary only, not official Semantic Equivalence Rate.
