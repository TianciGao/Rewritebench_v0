# Direct LLM Repair-1 Adapter Scaffold

Task: `direct_llm_repair_1_adapter_scaffold_v0`

This packet records the fake-provider-only scaffold for
`route_id=direct_llm_repair_1` and `method_id=direct_llm_repair_1`.

The scaffold consumes explicit Repair-1 context:

- original Direct LLM candidate SQL path
- original candidate id
- original run id
- execution/checker feedback JSON

It records secret-free metadata for `original_candidate_id`, `feedback_type`,
`repair_prompt_template_id`, `repaired_candidate_id`, provider/model
configuration, and extraction policy.

Boundary:

- No live LLM call was run.
- No DB execution, checker execution, timing, local metrics, SQLSolver, VeriEQL,
  official metrics, paper rendering, Track A 120, or live Repair-1 route was run.
- The Direct LLM original adapter was not modified.
- The unsupported Spark rows from the Direct LLM original frontier remain
  excluded from Repair-1.

Readiness:

- Fixture/fake-provider scaffold is ready.
- Future Repair-1 candidate scope remains the 13 actionable Direct LLM original
  frontier rows: `mismatch=10` and `candidate_execution_failed=3`.
- A live or facade Repair-1 run still requires separate authorization.
