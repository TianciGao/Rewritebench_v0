# Next Implementation Requirements

A future reusable POCR@planned / POCR@candidate aggregator should require a stable row-level diagnostic input schema with these fields:

- `case_id`, `pool`, `engine`, `method_id`, `route_id`, and denominator scope;
- candidate identity and candidate SHA binding;
- annotation status and fail-closed status;
- route mismatch and candidate mismatch flags;
- expected operation atom count from case-local root-level `skills.md`;
- Stage-B transformation-supported operation atom count;
- presence-only, insufficient-transformation-evidence, rejected-noop, and schema-invalid atom counts;
- diagnostic boundary flags.

The aggregator must extract expected atoms only from `operation_atom` entries in `skills.md`; semantic guard atoms are excluded from the operation coverage numerator and denominator.

It must apply fail-closed row handling for no candidate, generation failure, extraction failure, route mismatch, candidate mismatch, annotation missing, malformed JSON, timeout, provider failure, and schema-invalid rows after retry.

It must emit POCR@planned and POCR@candidate as diagnostic promotion-view candidates until separately authorized for official promotion.

It must keep POCR@curated as `NA` / `curated_manifest_missing` until a predeclared curated denominator manifest exists.

The output schema should include row-level `OC_i`, denominator inclusion flags, fail-closed status, route-level macro dry-run values, diagnostic micro-average only under a separate label, and official/paper boundary flags.

Test cases should cover complete candidate-bound routes, no-candidate rows, annotation-missing rows, schema-invalid rows, route mismatch rows, candidate mismatch rows, no-op control rows, rows with no expected operation atoms, and SQLGlot optimize missing-candidate rows.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
