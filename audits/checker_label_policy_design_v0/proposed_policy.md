# Proposed Policy

## Design Goals

- Do not globally ignore result-column labels.
- Preserve existing exact/mismatch semantics unless an explicit case/role policy says otherwise.
- Add visibility for label-only mismatches so local diagnostics can separate value mismatch from label mismatch.
- Keep explicit aliases strict by default.
- Avoid guessing generated-expression provenance from a result label string alone.

## Status Model

Add checker detail fields in a future patch:

```text
value_exact: true/false
label_exact: true/false
label_only_mismatch: true/false
label_policy: strict | diagnose_label_only | positional_values_only
label_mismatch_class: none | generated_expression_label_candidate | explicit_alias_or_unknown | mixed_or_unclassified
```

For the first implementation, keep the existing public status fields unchanged:

- `checker_status`
- `exact_status`
- `failure_bucket`

Under that behavior-preserving patch, a row with matching positional values but differing labels remains `mismatch`, but the mismatch artifact records `label_only_mismatch: true`.

## Policy Modes

`strict`

- Default.
- Labels are part of exactness.
- Values and labels must match after existing normalization.

`diagnose_label_only`

- Behavior-preserving.
- Labels are still part of exactness.
- If row counts and column counts match, and positional values match, but labels differ, the checker reports label-only details.
- Recommended first patch mode.

`positional_values_only`

- Explicit opt-in only.
- Row counts, column counts, and positional values decide exactness.
- Label differences are retained as warnings/details.
- Not recommended as a global default.

## Explicit Alias Policy

Explicit aliases should remain strict by default. A label mismatch involving an explicit alias should remain a mismatch unless the case config explicitly says labels are non-semantic.

The current checker cannot reliably determine explicit alias provenance from result JSONL labels alone. Any alias-aware relaxation needs one of:

- explicit case-local config;
- runner-supplied SQL/column provenance;
- a separately authorized SQL parser/provenance pass.

## Generated Expression Label Policy

Generated expression labels may vary by engine, function case, or formatting. They are good candidates for diagnostic warning rather than hard semantic mismatch, but only if values match positionally and row/column counts match.

Do not infer that a label is a safe generated expression solely from the label text. Treat it as `generated_expression_label_candidate` only for reporting unless config/provenance confirms the labels are non-semantic.

## Same-engine vs PORT

Do not make the policy pool-based. Use diagnostic role and case config:

- Same-engine rows: default strict, optional `diagnose_label_only`.
- Same-engine PORT real-adapter rows: same default strict behavior as other same-engine rows; keep separate from controlled PORT evidence.
- Controlled cross-dialect target-reference rows: keep existing manifest-gated positional comparison. Optionally add label warning details, but do not alter the already role-gated comparison.
- Unsupported/fail-closed rows: no checker label policy applies because checker is not attempted.
