# Semantic Equivalence Denominator Policy

This policy is local diagnostic only.

Denominator labels:
- `selected_rows`: rows selected by the source local diagnostic run.
- `exact_candidate_rows`: selected rows that are source executable, candidate generated, candidate executable, checker-successful, and exact/result-consistent.
- `verifier_eligible_exact_rows`: exact rows passing the feature-aware eligibility filter for the planned verifier pass.
- `verifier_attempted_rows`: eligible rows actually sent to VeriEQL.
- `decidable_rows`: `equivalent + non_equivalent`.
- `non_decidable_rows`: `unsupported + not_implemented + timeout + unknown + syntax_error + out_of_memory + tool_error + not_attempted`.

Local diagnostic rates:
- `local_diagnostic_semantic_equivalence_rate = equivalent / (equivalent + non_equivalent)` when `decidable_rows > 0`, else `null`.
- `verifier_decidability_rate = decidable_rows / verifier_attempted_rows` when `verifier_attempted_rows > 0`, else `null`.
- `verifier_eligibility_rate = verifier_eligible_exact_rows / exact_candidate_rows` when `exact_candidate_rows > 0`, else `null`.

Boundary:
- Do not call this official Semantic Equivalence Rate.
- Do not use local result-checker exactness as verifier equivalence.
- Do not include non-exact rows in verifier execution.
- Keep all unsupported/not-implemented/timeout/unknown/error rows visible and excluded from the decidable denominator.

