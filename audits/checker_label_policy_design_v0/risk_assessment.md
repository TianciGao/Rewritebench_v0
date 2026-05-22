# Risk Assessment

## Main Risks

Global label relaxation could hide real regressions. Explicit aliases often carry user-visible meaning, and changing them can be semantically relevant even when values match.

Generated expression labels are not reliably identifiable from result JSONL alone. A label string such as `AVG(x)` may look generated, but the checker lacks provenance to prove whether it came from an explicit alias, engine-generated expression, or adapter transformation.

Pool-based policy would be too coarse. PORT rows include controlled target-reference diagnostics, same-engine diagnostics, unsupported/fail-closed rows, and real-adapter behavior. These should not share a single label rule.

Changing `exact_status` would change local diagnostic counts. That may be useful later, but it must remain local-only and must not be presented as official metrics or paper evidence.

## Risk Controls

- Keep strict labels as the default.
- Add label-only visibility before allowing label relaxation.
- Require explicit case/role config for any exactness-changing label policy.
- Keep explicit aliases strict unless explicitly declared otherwise.
- Keep cross-dialect positional comparison manifest-gated.
- Require representative PERF, CONS, LONGTAIL, same-engine PORT, and controlled PORT regression tests.
- Keep all outputs local diagnostic only.

## Recommended Decision

Proceed only with a behavior-preserving diagnostic patch first. Defer any exactness-changing policy until a later task can define config ownership, validation rules, migration expectations, and regression coverage.
