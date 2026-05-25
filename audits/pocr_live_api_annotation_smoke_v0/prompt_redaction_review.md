# Prompt Redaction Review

Raw prompts were not stored.

Raw provider responses were not stored.

The audit packet stores:

- `prompt_sha256`
- `source_sql_sha256`
- `candidate_sql_sha256`
- safe annotation JSON for schema-valid responses
- safe provider status metadata
- bounded parse/error text for the malformed `PERF_0006` response

The prompt included case-local `skills.md` atom definitions, source SQL, candidate SQL, and optional positive/negative SQL context. That content was sent only to the configured OpenAI-compatible provider during the bounded smoke and was not copied into audit Markdown.

The structured annotation outputs are retained in `safe_annotation_outputs.jsonl` for audit review. They contain model rationales but no API keys or environment values.

The malformed `PERF_0006` raw provider content was not saved; only the JSON parser error was recorded.
