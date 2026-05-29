# Semantic Equivalence Policy

Current policy:

- Semantic Equivalence Rate remains `N.A.` without real formal verifier evidence.
- Local result-checker exactness must not substitute for verifier evidence.
- Synthetic summaries are tests and local diagnostics only; they are not official metric inputs.
- Unknown, timeout, unsupported, tool-error, and not-attempted outcomes are reported separately.
- Only `equivalent` and `non_equivalent` outcomes enter the decidable denominator.

Formula used by local verifier summaries:

```text
decidable_count = equivalent_count + non_equivalent_count
semantic_equivalence_rate = equivalent_count / decidable_count, when decidable_count > 0
```

If `decidable_count == 0`, then:

- `semantic_equivalence_rate=null`
- `semantic_equivalence_rate_status=not_applicable`
- `na_reason` must explain why the rate is not computable

Official-policy boundary:

- This closeout does not compute official Semantic Equivalence Rate.
- Promotion to official evidence requires a separate authorized task.
- Verifier evidence must remain route-aware, tool-aware, denominator-aware, and local-vs-official boundary-aware.
