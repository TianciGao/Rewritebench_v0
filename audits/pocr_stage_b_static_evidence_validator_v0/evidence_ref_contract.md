# Static Evidence Reference Contract

Supported diagnostic Stage B evidence refs are intentionally narrow:

- `candidate_sql_span:<literal substring>`: exact substring must occur in candidate SQL.
- `source_sql_span:<literal substring>`: exact substring must occur in source SQL.
- `positive_sql_span:<literal substring>`: exact substring must occur in positive SQL when available.
- `candidate_token_span:<normalized tokens>`: whitespace/case-insensitive normalized token span must occur in candidate SQL.
- `source_candidate_diff:changed`: confirms only that normalized source and candidate SQL text differ.

Rejected refs include unsupported prefixes, empty refs, LLM rationale, speedup/timing, taxonomy tags, checker exactness, and any malformed format. `validated_static_span` is diagnostic support only. It is not official POCR proof and cannot be promoted to paper-facing metrics without a later authorization.
