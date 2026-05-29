# Protected Surface Check

Allowed modified paths:

- `audits/verieql_feature_support_next_canary_selection_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected paths intentionally not modified:

- `src/`
- `tests/`
- `cases/`
- `case_sets/`
- `baselines/`
- `reports/`
- `results/`
- `output/`
- `benchmarks/`
- retained evidence
- `runs/user/`
- VeriEQL source tree

VeriEQL source tree status before writeback:

```text
## main...origin/main
 M constants.py
```

The `constants.py` modification was pre-existing and was not touched by this task.

Runtime artifacts:

- New `runs/user/` artifacts committed: no.
- New `output/` runtime artifacts committed: no.
- New real VeriEQL runtime output produced: no.

Observed release-repo changed paths during validation:

```text
project_control/MIGRATION_RUN_LOG.md
project_control/MIGRATION_STATUS.md
audits/verieql_feature_support_next_canary_selection_v0/README.md
audits/verieql_feature_support_next_canary_selection_v0/boundary_checklist.md
audits/verieql_feature_support_next_canary_selection_v0/candidate_pair_scan.csv
audits/verieql_feature_support_next_canary_selection_v0/command_log.md
audits/verieql_feature_support_next_canary_selection_v0/cons0007_unsupported_review.md
audits/verieql_feature_support_next_canary_selection_v0/next_canary_recommendation.md
audits/verieql_feature_support_next_canary_selection_v0/protected_surface_check.md
audits/verieql_feature_support_next_canary_selection_v0/verieql_feature_support_notes.md
```

Protected-surface violations: none.
