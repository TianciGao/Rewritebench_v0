# Fake Runtime Contract

## Fixture Response Schema

`SQLRB_LLM_R2_FAKE_RESPONSE` must be a JSON object. Supported success shapes:

```json
{"status": "ok", "candidate_sql": "SELECT ..."}
```

```json
{"status": "ok", "content": "Rules:\n- FilterMerge\nSQL:\nSELECT ...", "rule_sequence": ["FilterMerge"]}
```

Equivalent SQL fields are `candidate_sql`, `rewritten_sql`, `output_sql`,
`sql`, and `content`.

## Fake SQL Shape

`SQLRB_LLM_R2_FAKE_SQL` may contain exactly one raw SQL statement or one safe
SQL code fence.

## Fake Rule Sequence Shape

Rule sequence metadata may be supplied as:

- JSON list in `rule_sequence` / `rules`;
- comma-separated string;
- `SQLRB_LLM_R2_FAKE_RULE_SEQUENCE`.

Rule sequence is metadata only. It is not executable SQL.

## Supported Fake Statuses

- `ok`
- `success`
- `true`

Unsupported status values fail closed. `unsupported` and `not_supported` map to
an explicit unsupported fail-closed state.

## Runtime Boundary

Fake mode never calls a live LLM/API, network, DB, Java rule-system,
checkpoint, demonstration selector, verifier, or local metrics.
