# Semantic Equivalence Summary Review

Each timeout was written as an independent one-pair local verifier-support run.

Summary behavior by timeout:

| timeout_seconds | equivalent_count | non_equivalent_count | timeout_count | decidable_count | semantic_equivalence_rate | status |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| 30 | 0 | 0 | 1 | 0 | null | not_applicable |
| 120 | 0 | 0 | 1 | 0 | null | not_applicable |
| 300 | 0 | 0 | 1 | 0 | null | not_applicable |

All summaries preserved:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`
- `result_checker_exactness_used=false`

Interpretation:

- No official Semantic Equivalence Rate was computed.
- No Common-core, paper, retained-evidence, or leaderboard claim is supported by this probe.
- The local summaries correctly report N.A. because there were no decidable verifier outcomes.
