# Positive Control Gap Review

`positive_control_no_transformation_support` and `atom_or_positive_alignment_gap` rows are diagnostic gaps, not dropped rows. They may indicate skills.md atom wording, positive SQL alignment, prompt compliance, provider output quality, or Stage B evidence limitations. No official POCR numerator is computed from these rows.

- Positive-control rows: 40
- Positive-control transformation-supported operation atoms: 80
- Positive-control presence-only operation atoms: 10
- Positive-control insufficient-transformation-evidence operation atoms: 10
- Positive-control schema-invalid operation atoms: 7
- Positive-control zero-support cases: PERF_0024, PERF_0062, PORT_0024, LONGTAIL_0011
- Case-level atom/positive-alignment gaps: LONGTAIL_0011, PERF_0024, PERF_0062, PORT_0024

Gap Rows

| case_id | pool | expected_operation_atoms_count | transformation_supported | presence_only | insufficient_transformation_evidence | schema_invalid_atoms | calibration_risk |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| PERF_0024 | PERF | 3 | 0 | 0 | 0 | 3 | atom_or_positive_alignment_gap |
| PERF_0062 | PERF | 2 | 0 | 0 | 0 | 2 | atom_or_positive_alignment_gap |
| PORT_0024 | PORT | 2 | 0 | 0 | 0 | 2 | atom_or_positive_alignment_gap |
| LONGTAIL_0011 | LONGTAIL | 2 | 0 | 0 | 2 | 0 | atom_or_positive_alignment_gap |

Schema-invalid rows remain fail-closed and are visible in `annotation_schema_validation.csv`. They are not repaired and do not contribute to any diagnostic operation-support count.
