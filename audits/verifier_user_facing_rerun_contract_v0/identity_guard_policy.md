# Identity Guard Policy

Identity guard is required for every source-vs-candidate verifier row.

A candidate row may enter corrected `V_equiv` or `V_non` only if:

- source-vs-source normalizes to `equivalent`;
- candidate-vs-candidate normalizes to `equivalent`;
- source-vs-candidate normalizes to `equivalent` or `non_equivalent`.

If either identity check returns `unknown`, `timeout`, `unsupported`, `not_implemented`, `syntax_error`, `out_of_memory`, `tool_error`, `non_equivalent`, or `not_attempted`, the row must be excluded from corrected `V_equiv` and corrected `V_non`.

Semantic Equivalence Rate policy:

```text
SER = corrected_equivalent_count / (corrected_equivalent_count + corrected_non_equivalent_count)
```

The rate may be computed only when the corrected decidable denominator is greater than zero. Unknown, timeout, unsupported, not-implemented, syntax-error, OOM, tool-error, identity-failed, and not-attempted rows must be reported separately.

Local result-checker exactness is only an eligibility gate. It must never be substituted for formal verifier equivalence.
