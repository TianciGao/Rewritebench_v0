# common_core_sqlglot_noop_local_metrics_projection_v0

Verdict: `completed_with_fail_visible_limitations`

This packet records a non-official local metrics projection over existing Common-core SQLGlot noop local diagnostic snapshots.

Calculator command:

```bash
PYTHONPATH=src python scripts/dev/compute_local_user_metrics.py \
  --run runs/user/common_core_sqlglot_noop_postgres_snapshot \
  --run runs/user/common_core_sqlglot_noop_mysql_snapshot \
  --run runs/user/common_core_spark_sqlglot_noop_after_statement_patch
```

No Common-core rerun was performed. No new timing was collected. Metrics outputs were written only under ignored `runs/user/*/metrics/` directories and are not committed.

## Input Runs

- PostgreSQL: `runs/user/common_core_sqlglot_noop_postgres_snapshot`
- MySQL: `runs/user/common_core_sqlglot_noop_mysql_snapshot`
- Spark: `runs/user/common_core_spark_sqlglot_noop_after_statement_patch`

## Projection Summary

| Engine | selected | generated | candidate executable | exact | mismatch | Generation Rate | Execution Coverage Rate | Result Consistency Rate | speedup denominator |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PostgreSQL | 40 | 35 | 35 | 35 | 0 | 0.875 | 0.875 | 0.875 | 0 |
| MySQL | 40 | 40 | 39 | 31 | 8 | 1.0 | 0.975 | 0.775 | 0 |
| Spark | 40 | 40 | 33 | 31 | 2 | 1.0 | 0.825 | 0.775 | 0 |

Performance fields are `N.A.` for all three projections because the Common-core snapshot runs do not contain timing artifacts.

## Important Interpretation Notes

- These are local diagnostic metrics only, not official metrics or paper results.
- The calculator follows D033 formulas: Generation Rate is `candidate_generated / selected`, Execution Coverage Rate is `candidate_executable / selected`, and Result Consistency Rate is `exact / selected`.
- `preflight_passed` and `source_executable` remain diagnostics only.
- Semantic Equivalence Rate is `N.A.` without verifier evidence.
- Cross-Engine GM Speedup Ratio is `N.A.` without target-engine paired timing.
- POCR remains deferred with the external skill adapter pending.
- Regression@20 is not implemented.
- The current Common-core MySQL snapshot predates the label-only diagnostics patch, so projected `label_only_mismatch` is 0 even though later audits identified label-only candidates. The projection reports the existing snapshot artifacts as-is.

## Next Safe Action

Review whether the existing Common-core snapshots are sufficient for a non-official local diagnostic summary. If label-only diagnostics are required in the Common-core projection, separately authorize a targeted or bounded rerun that produces post-patch label diagnostic fields; do not infer them into the old snapshot.
