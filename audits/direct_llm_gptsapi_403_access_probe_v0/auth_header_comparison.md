# Auth Header Comparison

Both auth styles supported by the adapter/provider contract were tested with the same tiny chat-completions request and the explicit User-Agent.

```text
Authorization: Bearer <redacted>
status_code=200
classification=success
choices_present=true
```

```text
x-api-key: <redacted>
status_code=200
classification=success
choices_present=true
```

Interpretation: the observed `403 / 1010` is not explained by Bearer versus `x-api-key`. Both styles are accepted when the request includes `User-Agent: SQL-RewriteBench/0.1`.

