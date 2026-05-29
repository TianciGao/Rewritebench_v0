# Fake Runtime Contract

## Fixture Inputs

The fake runtime accepts either:

```bash
SQLRB_RBOT_FAKE_SQL="SELECT ..."
```

or a JSON object:

```json
{"status":"ok","candidate_sql":"SELECT ..."}
```

Accepted SQL fields are:

- `candidate_sql`
- `rewritten_sql`
- `output_sql`
- `sql`
- `content`

## Supported Fake Statuses

- `ok`
- `success`
- `true`

Unsupported or failed fake statuses fail closed.

## Boundary

Fake runtime mode never invokes:

- live LLM/API
- network
- RAG or Chroma
- CalciteRewrite
- DB execution
- checker
- timing
- verifier
- local metrics
