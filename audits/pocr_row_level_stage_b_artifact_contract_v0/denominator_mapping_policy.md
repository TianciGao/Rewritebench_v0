# Denominator Mapping Policy

POCR@planned uses planned POCR-eligible rows for the route and denominator scope. Missing candidates, generation failures, extraction failures, annotation missing, schema-invalid rows after retry, route mismatches, and candidate mismatches remain denominator members with `oc_i_fail_closed = 0`.

POCR@candidate uses rows with deterministic candidate binding. No-candidate rows are excluded from the candidate denominator, but annotation fail-closed rows, route mismatches, and candidate mismatches remain candidate-bound denominator rows when a candidate identity exists.

POCR@curated remains deferred until a predeclared curated manifest exists. It must remain `NA` / `curated_manifest_missing` without that manifest. POCR@curated remains deferred until a predeclared curated manifest exists.

Missing candidate handling:

- `no_candidate`, `generation_failed`, and `extraction_failed` contribute zero to POCR@planned.
- They do not enter POCR@candidate unless a valid candidate identity exists.

Annotation fail-closed handling:

- `malformed_json`, `provider_call_failed`, `timeout`, and `annotation_missing` contribute zero when the row is in a denominator.
- They remain explicit rows for audit and manual review.

Unsupported handling:

- Unsupported rows are retained with explicit status.
- Unsupported planned rows contribute zero to POCR@planned unless a later denominator manifest marks them outside the eligible scope.

No expected operation atoms handling:

- Rows with `expected_operation_atoms = 0` are `not_applicable_no_expected_operation_atoms`.
- They are counted separately and are not silently used as zero or one.

Route mismatch and candidate mismatch handling:

- Mismatches fail closed.
- They require manual review before any promotion.

SQLGlot optimize missing rows handling:

- Missing SQLGlot optimize candidates remain visible in POCR@planned with zero contribution.
- SQLGlot no-op candidates must not be substituted for SQLGlot optimize candidates.

No-op control handling:

- SQLGlot no-op remains a sanity/control route.
- Any transformation-supported operation atoms in a no-op route require manual review for possible over-accept before promotion.

Macro-average over per-row OC_i is required. Total supported atoms divided by total expected atoms is diagnostic micro-average only.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
