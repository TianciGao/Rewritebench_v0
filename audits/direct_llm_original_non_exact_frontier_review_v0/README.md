# Direct LLM Original Non-Exact Frontier Review

Task: `direct_llm_original_non_exact_frontier_review_v0`

Run reviewed: `direct_llm_original_track_a_120_canonical_v0`

Source material was limited to the canonical local metrics outputs under `runs/user/direct_llm_original_track_a_120_canonical_v0/metrics/` and the already-committed audit snapshots under `audits/direct_llm_original_track_a_120_canonical_user_rerun_v0/`.

No Repair-1 execution, live LLM call, benchmark rerun, new metric computation, official metric computation, paper result update, retained-evidence promotion, leaderboard output, denominator change, or case membership change was performed.

Frontier counts:

| bucket | rows |
| --- | ---: |
| semantic mismatch | 10 |
| candidate execution failed | 3 |
| unsupported engine | 5 |
| total non-exact frontier | 18 |

Repair-1 readiness verdict: design-ready for the 13 actionable rows in `mismatch` and `candidate_execution_failed`; not execution-ready until a separate Repair-1 implementation/run is explicitly authorized. The 5 `unsupported_engine` Spark rows should remain boundary rows and should not be sent to Repair-1 unless Spark/PORT support policy changes.
