# Semantic Equivalence Rate Policy

Semantic Equivalence Rate is a primary correctness metric.

Policy:

- SER is computed only from formal verifier evidence.
- Local result-checker exactness must not be used as verifier evidence.
- Source-vs-candidate verifier pairs are constructed only for rows that are already exact/result-consistent under the local checker or retained result-comparison protocol.
- Unknown, timeout, unsupported, not-implemented, tool-error, and no-verifier-support outcomes are excluded from the decidable SER denominator and reported separately.
- The decidable SER denominator is `equivalent + non_equivalent` verifier outcomes.
- Every route must report SER status as one of `computed`, `coverage_limited`, or `N.A.`.

Current repository alignment:

- `repository_spec/metrics_contract_v1.md` already limits SER to verifier-decidable result-consistent cases and says unknown/undecidable outcomes are reported separately.
- `src/sql_rewrite_bench/local_metrics.py` reports SER as not applicable with reason `formal_verifier_evidence_missing`; it does not substitute checker exactness for SER.
- `src/sql_rewrite_bench/verifier_support/summary.py` computes SER as `equivalent_count / decidable_count`, reports non-decidable counts separately, records `semantic_equivalence_source=formal_verifier_evidence`, and records `result_checker_exactness_used=false`.

Current gaps before paper-facing promotion:

- Verifier support currently reports `semantic_equivalence_rate_status` as `computed` or `not_applicable`; paper-facing policy should standardize `not_applicable` to `N.A.` and add `coverage_limited` when only a subset of exact/result-consistent rows receives decidable verifier evidence.
- Pair-schema validation accepts source-vs-candidate records but does not itself prove that a pair came from an exact/result-consistent row. The route-level verifier-pair construction step must enforce that eligibility.
- No current Direct LLM original canonical run has formal verifier evidence, so SER remains `N.A.` for that route.
