# Metric Mismatches Found

1. Result Consistency denominator:
   D032/latest paper and D033/local metrics use selected/planned rows; `metrics_contract_v1.md` still defines the denominator as executed candidate cases.

2. POCR vs Attribution Coverage:
   D032/latest paper uses Positive Operation Coverage Rate; `metrics_contract_v1.md` uses Attribution Coverage; local metrics defers POCR pending external skill adapter.

3. Cross-engine performance naming:
   D032/latest paper uses Cross-Engine GM Speedup Ratio; `metrics_contract_v1.md` uses Speedup Retention; local metrics defers cross-engine GM speedup until target-engine paired timing exists.

4. SER status vocabulary:
   Current verifier support uses `computed` / `not_applicable`; paper-facing policy should use `computed`, `coverage_limited`, or `N.A.`.

5. SER pair-construction eligibility:
   Policy requires source-vs-candidate verifier pairs only for exact/result-consistent rows. The current pair schema validates shape, not route-level eligibility.

No mismatch was found in the policy that local checker exactness must not be treated as formal semantic-equivalence evidence.
