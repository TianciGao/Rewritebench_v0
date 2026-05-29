# Direct LLM Repair-1

This directory contains the scaffold for the Direct LLM Repair-1 route:

- `route_id = direct_llm_repair_1`
- `method_id = direct_llm_repair_1`

Repair-1 consumes an original Direct LLM candidate plus explicit
execution/checker feedback and returns one repaired SQL candidate when the
provider response extracts unambiguously. It is a separate local diagnostic
route and never mutates Direct LLM original outputs.

## Adapter Command

```bash
python baselines/direct_llm_repair_1/adapter.py
```

Dry-run prompt rendering:

```bash
python baselines/direct_llm_repair_1/adapter.py --dry-run-prompt
```

## Environment Contract

The adapter uses the standard user adapter variables supplied by the D035
facade:

- `SQLRB_RUN_ID`
- `SQLRB_CASE_ID`
- `SQLRB_POOL`
- `SQLRB_ENGINE`
- `SQLRB_SOURCE_SQL_PATH`
- `SQLRB_CASE_DIR`
- `SQLRB_WORKSPACE_DIR`
- `SQLRB_CANDIDATE_SQL_PATH`

Repair-1 context must be explicit:

- `SQLRB_REPAIR1_ORIGINAL_CANDIDATE_SQL_PATH`
- `SQLRB_REPAIR1_FEEDBACK_PATH`
- `SQLRB_REPAIR1_ORIGINAL_CANDIDATE_ID`
- `SQLRB_REPAIR1_ORIGINAL_RUN_ID`

Aliases `SQLRB_ORIGINAL_CANDIDATE_SQL_PATH`, `SQLRB_REPAIR_FEEDBACK_PATH`, and
`SQLRB_FEEDBACK_PATH` are accepted for fixture/prototype integration.

Provider configuration follows the Direct LLM original adapter:

```bash
SQLRB_LLM_PROVIDER=openai_compatible
SQLRB_LLM_BASE_URL=https://api.gptsapi.net/v1
SQLRB_LLM_API_KEY=<secret>
SQLRB_LLM_MODEL=gpt-5.4
SQLRB_LLM_ALLOW_LIVE=1
```

`SQLRB_LLM_ALLOW_LIVE=1` is required for real provider calls. Fixture tests use
`SQLRB_LLM_PROVIDER=fake` and `SQLRB_LLM_FAKE_RESPONSE` or
`SQLRB_REPAIR1_FAKE_RESPONSE`; fake-provider mode does not make a live call.

## Feedback Contract

Supported Repair-1 feedback types:

- `checker_mismatch_feedback`
- `candidate_execution_error_feedback`

The adapter also accepts `mismatch` and `candidate_execution_failed` aliases in
fixture feedback JSON and normalizes them to the supported feedback types.

Excluded boundary feedback:

- `unsupported_engine_boundary_feedback`
- `unsupported_engine`

Unsupported Spark rows from the Direct LLM original frontier are excluded. The
current future Repair-1 candidate set is limited to 13 actionable rows:
`mismatch=10` and `candidate_execution_failed=3`.

## Prompt And Extraction Contract

Prompt template id:

```text
direct_llm_repair_1_feedback_sql_only_v0
```

Extraction policy id:

```text
single_sql_candidate_repair_v0
```

The prompt includes the source SQL, schema context, original candidate SQL,
original candidate id, feedback type, and local execution/checker feedback
summary. It never includes API key values.

Extraction accepts exactly one `SELECT` or `WITH` statement, optionally inside a
single SQL fenced block. Empty responses, prose, multiple SQL blocks, and
multiple SQL statements fail closed.

## Status Metadata

The adapter writes `direct_llm_repair_1_status.json` in `SQLRB_WORKSPACE_DIR`
with:

- `original_candidate_id`
- `feedback_type`
- `repair_prompt_template_id`
- `repaired_candidate_id`
- provider/model metadata
- extraction policy and extraction status
- local-only, non-official, non-paper, no-retained-evidence, and no-leaderboard
  flags

Secret values are not written.
