# Recommendation

Recommendation: `needs_separate_checker_policy_decision`.

The inspected rows should stay fail-visible under the current checker policy unless a separate task explicitly authorizes a narrow label-policy change.

## Findings

- `PERF_0062` is a same-engine non-PORT row. Its values match exactly, but aggregate expression labels differ by function-name case.
- `PORT_0004`, `PORT_0013`, `PORT_0022`, and `PORT_0024` are same-engine PORT rows in the SQLGlot noop real-adapter surface. Their values match exactly, but expression labels differ by formatting/spacing.
- No inspected row shows a value-level semantic mismatch.
- No inspected row requires numeric coercion, null normalization, row-order handling, or duplicate/multiplicity handling.
- This is not controlled PORT target-reference evidence and should not be mixed with those controlled diagnostics.

## Future Patch Guardrails

If a later task authorizes a checker label-policy patch, it should be explicit and narrow:

- Define whether generated expression labels may be ignored, normalized, or compared positionally.
- Preserve row-count and column-count strictness.
- Preserve value strictness unless an independently authorized normalization applies.
- Exclude arbitrary semantic value mismatches.
- Keep same-engine and cross-dialect behavior separately gated.
- Include regression cases for PERF, CONS, LONGTAIL, same-engine PORT, and controlled PORT target-reference paths.

If strict expression labels remain the intended policy, document these rows as expected fail-visible SQLGlot noop behavior and leave them mismatched.
