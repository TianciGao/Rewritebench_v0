# Test Fixture Plan

Future tests should include synthetic `pocr_stage_b_row_metrics.csv` fixtures for:

- normal schema-valid row with full support;
- no candidate row;
- malformed annotation row;
- provider failed row;
- timeout row;
- route mismatch row;
- candidate mismatch row;
- no expected operation atoms row;
- no-op control row with zero supported atoms;
- row with presence-only atoms but zero supported atoms;
- row with insufficient transformation evidence but zero supported atoms;
- row with supported atoms and partial `OC_i`;
- SQLGlot optimize missing candidate row;
- candidate-bound row with annotation missing;
- curated manifest missing row.

Expected assertions:

- POCR@planned includes planned fail-closed rows with zero contribution.
- POCR@candidate excludes no-candidate rows but retains candidate-bound fail-closed rows.
- POCR@curated remains `NA` without a curated manifest.
- Macro-average over per-row OC_i is required.
- Total supported atoms divided by total expected atoms is diagnostic micro-average only.
- Boundary flags remain non-promotional by default.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
