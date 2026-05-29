# Direct LLM Repair-1 No-Live 13-Frontier Dry Run

This audit packet records a fake-provider D035 user-facade dry run for `direct_llm_repair_1` over the 13 actionable Direct LLM original frontier rows.

Input frontier source: `audits/direct_llm_original_non_exact_frontier_review_v0/frontier_table.csv`.

Routes and runtime mode:

- route_id: `direct_llm_repair_1`
- method_id: `direct_llm_repair_1`
- provider: `fake`
- model_id: `gpt-5.4`
- live_call: `false`
- local_diagnostic_only: `true`

Counts:

- actionable rows selected: 13
- mismatch rows: 10
- candidate_execution_failed rows: 3
- unsupported_engine rows excluded: 5
- repaired candidates generated: 13
- preflight passed rows: 13
- fail-closed rows: 0

The facade was run in three engine-scoped commands so the selected set exactly matched the actionable frontier rows: one PostgreSQL row, eight MySQL rows, and four Spark rows. Unsupported Spark rows were not attempted.

No live LLM call, DB execution, checker, timing, `compute-local-metrics`, SQLSolver, VeriEQL, official metric, paper rendering, Track A 120, or Repair-1 live route occurred.

Next safe action: if accepted, authorize a tiny bounded live Repair-1 smoke over 3-6 actionable rows before any Repair-1 Track A 120 run.
