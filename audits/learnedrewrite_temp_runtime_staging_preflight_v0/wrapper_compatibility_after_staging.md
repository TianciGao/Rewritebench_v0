# Wrapper Compatibility After Staging

## HTTP Runtime

The staged runtime accepted a synthetic `POST /rewriter` request and returned
HTTP 200 parseable JSON with:

- `status=true`
- `message=SUCCESS`
- `data.rewritten_sql`

This confirms that the external runtime can produce a single candidate SQL
field when required relative rule assets are visible from the workdir.

## Request Schema

The working synthetic request used:

- `sql`: a string containing one artificial SQL query;
- `schema`: a string containing a JSON array of table metadata.

The source code inspected read-only uses `postInfo.getString("schema")` and then
`JSON.parseArray(schemaJson)`, so a future adapter HTTP mode should serialize
schema JSON as a JSON-array string unless a compatibility test proves array
payloads are accepted equivalently.

## Candidate Extraction

Future adapter extraction should target:

```text
data.rewritten_sql
```

The synthetic result was exactly one SQL statement and is compatible with the
existing single-SQL extraction policy in principle.

## Remaining Adapter Gap

`baselines/learnedrewrite/adapter.py` currently has fail-closed real `http` and
`cmd` hooks. No adapter code was changed in this task. A user-facade
external-runtime smoke still needs a separately authorized implementation that:

- gates runtime use with `SQLRB_LEARNEDREWRITE_ALLOW_RUNTIME=1`;
- posts to the configured local URL;
- serializes schema JSON correctly;
- extracts `data.rewritten_sql`;
- records no secrets;
- fails closed on missing, malformed, empty, or multiple-SQL responses.

Wrapper compatibility verdict: runtime response contract is compatible enough
to authorize narrow HTTP-mode adapter work, but current adapter code is not yet
ready for a real external-runtime user-facade smoke.
