# Semantic Equivalence Denominator Policy

This task defines only local diagnostic denominator labels for a future verifier pass. It does not compute official Semantic Equivalence Rate.

Definitions:

- selected rows: all rows selected by the source run
- exact candidate rows: selected rows that passed source execution, candidate generation, candidate execution, checker success, and exact/result-consistency
- bound4 verifier-eligible exact rows: exact rows that are feature-eligible under `finite_bound_bound4_timeout30_cores1`
- proposed verifier-attempt rows: the rows selected for the next bounded pass
- decidable rows: `equivalent + non_equivalent`
- non-decidable rows: `unsupported`, `not_implemented`, `timeout`, `unknown`, `syntax_error`, `out_of_memory`, `tool_error`, and `not_attempted`

Local diagnostic rates for a future pass:

- `local_bound4_subset_semantic_equivalence_rate = equivalent_count / decidable_count` when `decidable_count > 0`
- `verifier_decidability_rate = decidable_count / verifier_attempted_rows` when `verifier_attempted_rows > 0`
- `verifier_eligibility_rate = bound4_verifier_eligible_exact_rows / exact_candidate_rows` when `exact_candidate_rows > 0`

Boundary rules:

- Do not call the local diagnostic rate official Semantic Equivalence Rate.
- Do not mix bound-4 and bound-10 rows in one denominator.
- Do not substitute local result checker exactness for verifier equivalence.
- Do not promote local diagnostic output into top-level `reports/`, `results/`, or retained evidence without a separate authorized task.
