# Paper Boundary Recommendation

Recommendation: do not promote this VeriEQL ledger to paper-facing Semantic Equivalence Rate.

Reasons:

- Only 4 of 35 exact rows passed identity sanity.
- 31 exact rows failed source-vs-source or candidate-vs-candidate identity sanity.
- Corrected decidable coverage over exact rows is 4/35.
- `LONGTAIL_0023` remains a VeriEQL identity failure, not candidate semantic drift evidence.

Paper-facing Semantic Equivalence Rate remains blocked and coverage-limited.

Future paper-facing use would require:

- an approved identity-guard policy,
- higher verifier decidability and identity-pass coverage,
- clear handling of unsupported, not-implemented, timeout, and tool-error rows,
- independent investigation of VeriEQL identity failures,
- or corroboration from another verifier such as SQLSolver.
