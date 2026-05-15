# Validation Draft Notes

`PORT_0004` has not been validated yet.

This directory now contains draft executable-looking validation scaffolding:

- `load_witness_pg.sql`
- `load_witness_mysql.sql`
- `load_witness_spark.sql`
- `run_pg_validation.sh`
- `run_mysql_validation.sh`
- `run_spark_validation.sh`
- `check_results.py`

This is a cross-dialect portability validation model.

- `source.sql` is MySQL-shaped source SQL for this case.
- `source.sql` should be executed only in MySQL to produce the semantic reference output.
- PostgreSQL and Spark should execute only their target rewrite files.

A later validation task should:

1. run MySQL source reference generation with `run_mysql_validation.sh`,
2. run PostgreSQL target rewrites with `run_pg_validation.sh`,
3. run Spark target rewrites with `run_spark_validation.sh`,
4. run `check_results.py` against the five generated TSV files,
5. inspect the generated `runs/<engine>/` outputs,
6. treat any success as draft evidence only until registry writeback is explicitly requested.

Status remains draft-only, not executed, not validated, and not registered.

No engine commands have been run for this draft package in the current task.
