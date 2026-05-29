# Paper Boundary

This packet is local diagnostic evidence only.

It does not compute official metrics, does not compute Semantic Equivalence Rate, does not compute formal Regression@20, does not update paper reports/results, and does not promote retained evidence.

The route card uses selected rows as the denominator for local diagnostic coverage fields:

- `local_generation_rate = generated_candidate_rows / selected_rows`
- `local_execution_coverage_rate = candidate_executable_rows / selected_rows`
- `local_result_consistency_rate = exact_rows / selected_rows`

Speedup diagnostics are computed only over exact timed rows. They are suitable for local comparison planning against the refreshed Calcite HEP PostgreSQL route card, but they are not paper-facing metric values.
