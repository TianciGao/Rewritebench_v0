# Route-Level Aggregation Policy

Route-level aggregation is not executed in this task.

Route-level aggregation is allowed only after official promotion implementation is separately authorized.

Future aggregation must include at least:

- `planned_pocr_eligible_rows`
- `candidate_bound_rows`
- `annotation_attempted_rows`
- `schema_valid_rows`
- `fail_closed_rows`
- `no_candidate_rows`
- `route_mismatch_rows`
- `candidate_mismatch_rows`
- `expected_operation_atoms`
- `stage_b_supported_operation_atoms`
- `POCR@planned`
- `POCR@candidate`
- `POCR@curated`, reported as `NA` / `curated_manifest_missing` until a predeclared curated manifest exists

For SQLGlot optimize missing candidates, missing rows remain in POCR@planned with zero contribution. SQLGlot no-op candidates must not be substituted for SQLGlot optimize candidates.

The SQLGlot no-op route remains a sanity/control route. If a no-op route produces transformation-supported operation atoms, those atoms must enter manual review for possible over-accept before any promotion.

Stage A annotation alone is not counted. Stage B transformation-aware validation is required. Semantic guard atoms are excluded from the operation coverage numerator and denominator.

No route-level POCR score is emitted in this task. No paper-facing metric is promoted in this task. No global leaderboard is produced.
