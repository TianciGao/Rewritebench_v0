# PORT_0004 Plan Collection

This directory contains plan-collection scaffolding for `PORT_0004`.

Current status boundary:
- `PORT_0004` remains a draft-only PARROT / BIRD portability case.
- Cross-dialect result evidence is tracked separately in `runs/result_check.json`.
- Plan collection is prepared here, but not yet executed by this task.
- No admission, formal review completion, or release-grade claim is implied.

## Cross-Dialect Plan Model

`PORT_0004` treats MySQL as the source-reference engine.

Planned plan collection scope:
- MySQL collects a plan for `source.sql` only.
- PostgreSQL collects plans for `rewrite_pos_01.sql` and `rewrite_neg_01.sql` only.
- Spark collects plans for `rewrite_pos_02_spark.sql` and `rewrite_neg_02_spark.sql` only.

This scaffold intentionally does not try to run `source.sql` on PostgreSQL or Spark.

## Expected Outputs After Later Manual Execution

- `runs/mysql/plans/source.json`
- `runs/pg/plans/rewrite_pos_01.json`
- `runs/pg/plans/rewrite_neg_01.json`
- `runs/spark/plans/rewrite_pos_02_spark.txt`
- `runs/spark/plans/rewrite_neg_02_spark.txt`
- `runs/plan_check.json`

## Future Manual Run Order

Recommended manual order for later execution:
1. Run `validation/collect_mysql_plans.sh`.
2. Run `validation/collect_pg_plans.sh`.
3. Run `validation/collect_spark_plans.sh`.
4. Run `python validation/check_plan_artifacts.py`.

The final checker only verifies plan-artifact presence. It does not review plan semantics and does not change registry or review status.
