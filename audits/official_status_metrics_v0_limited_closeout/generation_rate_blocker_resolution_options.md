# Generation Rate Blocker Resolution Options

## Current Blocker

Generation Rate remains blocked by `inferred_generated_policy_not_official_and_sqlglot_generated_ready_gap`. The limited official status metrics task did not compute official Generation Rate. The status inference overlay contains 94 R1 `inferred_generated=true` rows, but those rows are not official observed-generated evidence.

## Option A: Keep Generation Rate Blocked Until Observed Generated Evidence Improves

This is conservative and preserves the Metrics Contract v1 meaning of emitted candidate SQL. It avoids converting readiness or checker-derived artifacts into generation evidence. The drawback is that public status reporting remains incomplete.

## Option B: Authorize Inferred Generated As Official Generation Rate Support With Strict Labeling

This would allow some ready-implies-generated rows to contribute to official Generation Rate. It requires a separate policy decision, source-specific semantics, and strict observed-vs-inferred labeling. It is riskier because readers may treat inferred generated evidence as source-observed generation.

## Option C: Create Separate Generation/Readiness Diagnostic Table, Not Primary Generation Rate

This can expose useful readiness/generation-adjacent evidence without changing the primary Generation Rate definition. It is safer than officializing inference, but it still requires renderer authorization and clear non-primary labeling.

## Option D: Collect More SQLGlot Generated/Ready Evidence Before Officializing

This preserves the official Generation Rate boundary and targets the largest known evidence gap. It should use only sanitized non-timing sources with row grain proven at case_id x engine x rewrite_method.

## Recommendation

The safest next action is Option D, with Option C as an optional diagnostic-only companion if a future renderer is authorized. Do not officialize Generation Rate from inferred fields until observed generated evidence and SQLGlot generated/ready semantics are resolved.
