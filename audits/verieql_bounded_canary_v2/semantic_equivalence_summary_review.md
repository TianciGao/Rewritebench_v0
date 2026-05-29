# Semantic Equivalence Summary Review

Summary policy:

- `decidable_count = equivalent_count + non_equivalent_count`
- `semantic_equivalence_rate = equivalent_count / decidable_count` only when `decidable_count > 0`
- if `decidable_count == 0`, `semantic_equivalence_rate=null`
- unavailable VeriEQL sets `na_reason=verieql_unavailable`
- local result-checker exactness is not used as verifier equivalence

Fail-closed smoke result:

```text
tool_available=False
semantic_equivalence_rate_status=not_applicable
na_reason=verieql_unavailable
not_attempted_count=1
```

Fake-command test result:

- a test-only fake command produced `equivalent`
- local synthetic summary produced `semantic_equivalence_rate=1.0`
- this was not a real VeriEQL run and not official Semantic Equivalence Rate
