# Future Aggregator Requirements

The future aggregator should validate inputs before computing any dry-run or promoted view.

Input validation:

- Required columns are present.
- Boolean and status values use allowed vocabularies.
- `case_id`, `pool`, `engine`, `method_id`, `route_id`, and denominator scope match the planned denominator manifest.
- Candidate-bound rows have candidate id, path, and SHA.
- `skills_md_sha256` is present for every row.
- Atom counts are non-negative and internally consistent.
- Boundary constants are present and safe.

Route and candidate binding checks:

- Route mismatch rows fail closed.
- Candidate mismatch rows fail closed.
- Candidate SHA mismatches require manual review.

Denominator manifest checks:

- POCR@planned requires planned denominator rows.
- POCR@candidate requires candidate-bound rows.
- POCR@curated remains `NA` unless a curated manifest is supplied.

Computation:

- Compute macro-average over `oc_i_fail_closed`.
- Compute POCR@candidate over candidate-bound denominator rows only.
- Report diagnostic micro-average only when explicitly requested and clearly labeled.

Output route summary schema should include planned rows, candidate-bound rows, annotation attempted rows, schema-valid rows, fail-closed rows, no-candidate rows, route mismatch rows, candidate mismatch rows, expected operation atoms, Stage-B-supported operation atoms, POCR@planned, POCR@candidate, POCR@curated status, diagnostic micro-average if requested, and boundary flags.

Tests should cover complete rows, fail-closed rows, no-candidate rows, mismatch rows, unsupported rows, no-op control rows, SQLGlot optimize missing candidate rows, and no-expected-operation-atom rows.

Macro-average over per-row OC_i is required. Total supported atoms divided by total expected atoms is diagnostic micro-average only.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
