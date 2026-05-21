# Checker Normalization Boundary

Opt-in cross-dialect checker normalization is enabled only for manifest-resolved cross-dialect local diagnostics where the checker comparison is `source_reference_result_to_target_candidate_result`.

Implemented cross-dialect-only normalization scope:

- Positional column comparison after strict JSON object equality fails, only when row counts and column counts match.
- Decimal string equivalence using safe decimal parsing for numeric-looking string pairs.

The policy does not broaden date/time conversion, boolean conversion, NULL conversion, ordering policy, multiset policy, SQL semantic verification, timing, speedup, or official metric computation.

Same-engine behavior is preserved. PERF, CONS, LONGTAIL, and same-engine PORT routes are not automatically switched to positional comparison or decimal relaxed comparison. This boundary is recorded in `audits/port_cross_dialect_checker_normalization_v0/` and remains local diagnostic only.
