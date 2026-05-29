# Normalized Verdict Review

Normalization policy:

- Clean equivalent requires no `TMO`, no `unknown`, no `tool_error`, and no `unsupported` marker.
- Any `TMO` state keeps the row normalized as `timeout`.
- Partial `EQU+TMO` is not reinterpreted as `equivalent`.
- Local result-checker exactness is not used as verifier evidence.

Probe results:

```text
timeout=30: normalized_verdict=timeout
timeout=120: normalized_verdict=timeout
timeout=300: normalized_verdict=timeout
```

No clean equivalent verdict was obtained.

Final classification:

```text
equivalent_path_timeout_or_internal_subcheck_timeout
```

The existing wrapper behavior is appropriate for this evidence: it preserves the timeout and does not overstate partial `EQU` states as formal equivalence.
