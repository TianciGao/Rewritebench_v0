# Verifier-Phase SER Boundary

Semantic Equivalence Rate is a primary correctness metric.

SER requires formal verifier evidence:

```text
SER = |V_equiv| / |V_equiv union V_non|
```

Boundary:

- Local result checker exactness is not SER.
- Local result-checker exactness must not be used as SER evidence.
- The verifier phase should operate over exact/result-consistent source-vs-candidate pairs.
- Unknown, timeout, unsupported, not_implemented, tool_error, no_verifier_support, and not_attempted outcomes are excluded from the decidable SER denominator and reported separately.
- Every route must report SER status as `computed`, `coverage_limited`, or `N.A.`.
- SQLSolver and VeriEQL are support/verifier tools, not rewrite baselines.
- Verifier outputs must remain separate from method-generated candidate failures and package hard-negative checker controls.
- Verifier limitations must not be counted as method rewrite failures.

No official SER is produced by this contract patch.
