# Route Binding And Replay Policy

Replay requires exact binding across:

- `case_id`
- `engine`
- `method_id`
- `route_id`
- `candidate_rel_path`
- `candidate_sha256`
- `skills_contract_hash` or `skills_md_sha256`
- `case_set_id`
- `denominator_scope`

Route mismatch must fail closed. Method mismatch must fail closed. Case mismatch must fail closed. Engine mismatch must fail closed. candidate_sha256 mismatch must fail closed. Skills contract mismatch must fail closed unless a separately authorized migration policy exists.

## Matching-Route Replay

Candidate route:

```text
direct_llm_original_pg40_pocr_diagnostic
```

Annotation route:

```text
direct_llm_original_pg40_pocr_diagnostic
```

If case, engine, method, route, candidate SHA, and skills contract all match, the annotation row may be accepted as diagnostic input for schema and Stage B processing.

## Route-Mismatch Replay

Candidate route:

```text
direct_llm_original_pg40_user_replay
```

Annotation route:

```text
direct_llm_original_pg40_pocr_diagnostic
```

This must fail closed as `route_mismatch`. Annotation artifacts are not reusable across arbitrary route labels.

## Candidate SHA Mismatch

If `candidate_rel_path` resolves but the current candidate file SHA-256 does not match `candidate_sha256` in the annotation row, replay must fail closed as `candidate_mismatch`.

This protects annotation evidence from being replayed against a modified or unrelated candidate SQL file.
