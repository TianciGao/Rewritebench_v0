# Direct LLM Repair-1 Track A 120 Route Assembly Policy

This packet defines how the future `direct_llm_repair_1` Track A 120 local diagnostic route should assemble final candidates from Direct LLM original outputs plus at most one Repair-1 attempt on eligible frontier rows.

The policy is needed because Direct LLM + Repair-1 is a separate route from Direct LLM original. It must not be merged into Direct LLM original metrics, and it must retain the same Track A same-engine denominator of 120 planned rows.

Policy verdict:

- Repair-1 route semantics are defined for all 120 planned rows.
- Original exact rows use the Direct LLM original candidate as the final candidate.
- Original `mismatch` and `candidate_execution_failed` rows may receive one Repair-1 attempt.
- Original `unsupported_engine` rows are not attempted and remain visible boundary rows.
- Final candidate execution, checker, timing, and future local metrics must be produced by the Repair-1 route run itself, not copied as official metrics from the 13-row diagnostic.

Evidence basis:

- Direct LLM original canonical Track A 120 local diagnostic selected 120 rows, generated 120 candidates, produced 102 exact rows, 10 mismatch rows, 3 candidate-execution-failed rows, and 5 unsupported-engine rows.
- Repair-1 no-live dry run selected the 13 actionable rows and excluded the 5 unsupported rows.
- Repair-1 bounded live 13-row diagnostic selected 13 rows, generated 13 repaired candidates, produced 13 candidate-executable rows, 9 exact rows, 4 mismatch rows, 0 candidate-execution-failed rows, and 9 timed exact rows.

Boundary:

- No Track A 120 run occurred in this task.
- No live LLM call, DB execution, checker execution, timing collection, local metrics, verifier, official metric, paper rendering, retained-evidence promotion, or leaderboard generation occurred.
- This policy does not change denominator, case membership, paper results, retained evidence, or raw legacy evidence.

Next safe action:

Authorize the Direct LLM + Repair-1 Track A 120 canonical local diagnostic run using the route assembly policy here, then compute non-official local metrics with `src/sql_rewrite_bench/local_metrics.py` through the user facade. Do not promote results to paper or retained evidence without a separate promotion task.
