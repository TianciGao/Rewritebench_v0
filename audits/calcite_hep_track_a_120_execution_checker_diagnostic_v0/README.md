# Calcite HEP Track A 120 Execution/Checker Diagnostic

Task: `calcite_hep_track_a_120_execution_checker_diagnostic_v0`

Branch: `feature/case-package-v2-external-schema`

Route:

- `route_id = calcite_hep_fail_closed`
- `method_id = calcite_hep_fail_closed`
- adapter: `baselines/calcite_hep_fail_closed/adapter.py`

This packet records a local-only D035 user-facade execution/checker diagnostic
over Common-core v0 Track A: 40 cases x PostgreSQL/MySQL/Spark = 120 planned
rows.

The run selected all 120 planned rows. It generated 99 candidates, executed 98
source rows and 95 candidate rows, attempted checker comparison on 95 rows, and
found 81 exact/result-consistent rows.

This is not a timing run, not a canonical metrics run, not official evidence,
and not paper-facing.
