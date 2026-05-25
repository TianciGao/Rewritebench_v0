# Prompt Alignment Review

- `candidate_sql_span:<literal substring>` present: true
- `source_sql_span:<literal substring>` present: true
- `positive_sql_span:<literal substring>` present: true
- `candidate_token_span:<normalized tokens>` present: true
- `source_candidate_diff:changed` present: true
- Unsupported-ref rejection warning present: true
- JSON-only requirement present: true
- Taxonomy inference prohibition present: true

The prompt now tells Stage A to emit only Stage-B-supported static evidence refs and to use empty evidence_refs when no supported ref exists.
