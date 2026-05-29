# Direct LLM Original

This directory contains the D035 user-facing adapter scaffold for:

- `route_id = direct_llm_original`
- `method_id = direct_llm_original`

The adapter is provider-agnostic and uses the public `sqlrb user evaluate`
adapter environment contract. It generates candidates only; it does not execute
SQL, run checkers, collect timing, compute metrics, update paper reports/results,
promote retained evidence, or create leaderboard output.

## Adapter Command

```bash
python baselines/direct_llm_original/adapter.py
```

Dry-run prompt rendering:

```bash
python baselines/direct_llm_original/adapter.py --dry-run-prompt
```

## Environment Contract

Required user-run variables are supplied by `sqlrb user evaluate`:

- `SQLRB_RUN_ID`
- `SQLRB_CASE_ID`
- `SQLRB_POOL`
- `SQLRB_ENGINE`
- `SQLRB_SOURCE_SQL_PATH`
- `SQLRB_CASE_DIR`
- `SQLRB_WORKSPACE_DIR`
- `SQLRB_CANDIDATE_SQL_PATH`

Provider configuration is environment-variable based only:

```bash
SQLRB_LLM_PROVIDER=openai_compatible
SQLRB_LLM_BASE_URL=https://api.gptsapi.net/v1
SQLRB_LLM_API_KEY=<secret>
SQLRB_LLM_MODEL=gpt-5.4
SQLRB_LLM_TEMPERATURE=0
SQLRB_LLM_TOP_P=1
SQLRB_LLM_MAX_TOKENS=2048
SQLRB_LLM_TIMEOUT=60
SQLRB_LLM_ALLOW_LIVE=1
```

GPTSAPI aliases are also accepted:

```bash
GPTSAPI_API_KEY=<secret>
GPTSAPI_BASE_URL=https://api.gptsapi.net/v1
GPTSAPI_MODEL=gpt-5.4
```

`SQLRB_LLM_ALLOW_LIVE=1` is required for a real provider call. Without it, the
adapter fails closed with `live_api_disabled`. API keys are never written to
status metadata.

Fake-provider smoke:

```bash
SQLRB_LLM_PROVIDER=fake \
SQLRB_LLM_FAKE_RESPONSE='```sql
SELECT 1 AS ok;
```' \
python baselines/direct_llm_original/adapter.py
```

## Prompt Contract

The prompt asks for one semantically equivalent SQL rewrite for the target
same-engine dialect, SQL only, no explanation, using the provided schema. If no
safe rewrite is possible, the model is instructed to return the original SQL
unchanged.

Prompt template id:

```text
direct_llm_original_sql_only_v0
```

## Extraction Contract

Extraction policy id:

```text
single_sql_candidate_v0
```

Rules:

- Prefer a single fenced SQL block if exactly one is present.
- Otherwise accept the full response if it looks like one `SELECT` or `WITH`
  statement.
- Reject empty responses, non-SQL prose, multiple SQL blocks, and multiple SQL
  statements.
- Do not repair or rewrite the candidate in this route.

## Status Metadata

The adapter writes `direct_llm_status.json` in `SQLRB_WORKSPACE_DIR` with:

- provider and `base_url_host`
- model id, temperature, top_p, max_tokens, timeout
- prompt template id and extraction policy
- request timestamp
- raw response saved flag/path
- candidate generation status and failure bucket
- local-only and non-official boundary flags

Secret values are not written.
