# Patch Options

## Option A: Behavior-preserving label-only diagnostics

Add value/label diagnostic details without changing exactness.

Behavior:

- Existing exact rows stay exact.
- Existing value mismatches stay mismatch.
- Label-only rows stay mismatch but gain details:
  - `value_exact: true`
  - `label_exact: false`
  - `label_only_mismatch: true`

Pros:

- Low risk.
- Does not change exact counts.
- Gives users and future audits better failure classification.
- Does not require config migration.

Cons:

- The five MySQL rows remain fail-visible until a separate policy decision.

Recommendation: first implementation choice.

## Option B: Case-local strict/diagnose/positional label policy

Add explicit config, probably under `compare_config.yaml`:

```yaml
result_comparison:
  column_label_policy:
    label_policy: diagnose_label_only
```

Possible modes:

- `strict`
- `diagnose_label_only`
- `positional_values_only`

Pros:

- Explicit and auditable.
- Can keep default strict while letting selected cases declare non-semantic labels.

Cons:

- Requires checker config updates and validator/schema support.
- `positional_values_only` can hide alias mistakes if applied too broadly.

Recommendation: consider only after Option A is in place and reviewed.

## Option C: Generated-expression-aware policy

Implement a policy such as:

```yaml
result_comparison:
  column_label_policy:
    label_policy: ignore_generated_expression_labels
```

Pros:

- Closest to the observed MySQL failure shape.

Cons:

- The checker cannot prove generated-expression provenance from JSONL result labels alone.
- Requires either explicit case config, SQL parsing, or engine metadata.
- Parser/provenance additions broaden checker responsibility.

Recommendation: do not implement until provenance rules are separately designed.

## Option D: Globally ignore labels

Compare all rows positionally by default.

Pros:

- Would resolve label-only mismatches broadly.

Cons:

- High risk.
- Hides explicit alias regressions.
- Changes same-engine semantics globally.
- Changes exact counts without case-local authorization.

Recommendation: reject.
