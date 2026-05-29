# Implementation Summary

Files changed:

- `baselines/direct_llm_repair_1/adapter.py`
- `baselines/direct_llm_repair_1/README.md`
- `tests/user_entry/test_direct_llm_repair_1_adapter.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

The new adapter scaffold follows the Direct LLM original adapter shape while
remaining a separate route. It reads source SQL from the user adapter
environment, reads the original Direct LLM candidate from an explicit path, and
reads Repair-1 feedback from an explicit JSON fixture/input path.

Implemented behavior:

- Prompt template id: `direct_llm_repair_1_feedback_sql_only_v0`.
- Extraction policy: `single_sql_candidate_repair_v0`.
- Supported feedback: `checker_mismatch_feedback` and
  `candidate_execution_error_feedback`.
- Excluded feedback: `unsupported_engine_boundary_feedback`.
- Fake provider support through `SQLRB_LLM_PROVIDER=fake`.
- Live provider calls remain gated by `SQLRB_LLM_ALLOW_LIVE=1` and an API key.
- Secret values are not written to prompt, status, raw response, or candidate
  artifacts.

Fail-closed behavior:

- missing original candidate
- missing or malformed feedback
- unsupported feedback
- unsupported-engine boundary rows
- unsupported provider
- missing live gate/API key for live provider mode
- provider request failure
- empty/prose/multiple-SQL extraction failure

This task did not implement a facade Repair-1 run and did not execute Repair-1
against benchmark rows.
