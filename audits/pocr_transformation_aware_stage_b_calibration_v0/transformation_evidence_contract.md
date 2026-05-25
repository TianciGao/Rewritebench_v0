# Transformation Evidence Contract

For `operation_atom` rows, Stage B requires transformation-aware evidence rather than span presence alone. `candidate_sql_span`, `source_sql_span`, or `positive_sql_span` alone is `presence_only` and cannot count as transformation support. A row may become `transformation_supported` only when a candidate-specific or positive-aligned span is paired with `source_candidate_diff:changed`. Source-like/no-op candidates are classified as `presence_only` or `rejected_noop_equivalent`. This is diagnostic support only and is not official POCR proof.
