# Table 2. Failure Frontier Summary

This table is diagnostic only. It is not a Candidate Failure Rate table and does not compute new rates.

| method_or_route | scope | exact_count | mismatch | candidate_execution_failed | fail_closed_or_no_candidate | unsupported | source_like_or_noop | timing_ineligible_exact | key_frontier_cases |
|---|---|---:|---:|---:|---:|---:|---|---:|---|
| direct_llm_original | Track A same-engine 120 planned rows | 102 | 10 | 3 | 0 | 5 | not_summarized | 12 | Direct LLM original frontier includes 10 mismatches, 3 candidate execution failures, and 5 unsupported Spark rows. |
| direct_llm_repair_1 | Track A same-engine 120 planned rows | 111 | 4 | 0 | 0 | 5 | not_summarized | 13 | Remaining mismatches are `PORT_0004/mysql`, `PORT_0013/mysql`, `PORT_0022/mysql`, and `PORT_0024/mysql`; unsupported Spark rows remain denominator-visible. |
| sqlglot_noop | Track A same-engine 120 planned rows | 97 | 10 | 3 | 5 | 5 | not_summarized | 0 | Compact packet records mismatch, adapter-failed, unsupported, and candidate-execution frontiers. |
| sqlglot_optimize_schema_aware | Track A same-engine 120 planned rows | 66 | 25 | 9 | 15 | 5 | not_summarized | 0 | Schema-aware optimization broadens mismatch and execution-failure frontiers. |
| calcite_hep_fail_closed | Track A same-engine 120 planned rows | 81 | 14 | 3 | 21 | 1 | not_summarized | 1 | Fail-closed/no-candidate rows dominate the Calcite HEP frontier. |
| learnedrewrite | PostgreSQL-only PG40 bounded diagnostic | 17 | 6 | 6 | 11 | 0 | 2 | 0 | LearnedRewrite has mismatch, execution-failed, and fail-closed/no-candidate PG40 frontier rows. |
| rbot_gpt54_adapted | PostgreSQL-only PG40 bounded diagnostic | 37 | 1 | 2 | 0 | 0 | 0 | 4 | `PORT_0013` mismatch; `PERF_0008` and `LONGTAIL_0011` candidate execution failed. |
| llm_r2_gpt54_adapted | PostgreSQL-only PG40 bounded diagnostic | 39 | 0 | 1 | 0 | 0 | 1 | 5 | `LONGTAIL_0011` candidate execution failed; `CONS_0037` is source-like/no-op diagnostic. |

Full paths and boundaries are in `table2_failure_frontier_summary.csv`.
