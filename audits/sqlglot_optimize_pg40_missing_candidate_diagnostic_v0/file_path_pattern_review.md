# File Path Pattern Review

Expected SQLGlot optimize PostgreSQL PG40 candidate path pattern:

`output/results/sqlglot_optimize_schema_aware_track_a_120_user_reproduction_v0/candidate_sql/sqlglot_optimize_schema_aware/sqlglot_optimize_schema_aware_track_a_120_user_reproduction_v0/postgres/<CASE_ID>__postgres.sql`

The selected root uses the expected D035-style method/route/engine path and the expected `<CASE_ID>__postgres.sql` filename shape for the 34 present PostgreSQL files.

The six target cases are absent from disk in the selected PostgreSQL root and are also absent from the prior SQLGlot optimize PostgreSQL capture/export/canonical roots. They are not merely absent from the manifest: the manifest rows exist and mark them `generation_failed` / `not_generated` / `adapter_failed`.

Selected-manifest cross-engine presence for the six cases:

- `CONS_0009`: postgres=false, mysql=false, spark=false
- `PORT_0004`: postgres=false, mysql=true, spark=true
- `PORT_0013`: postgres=false, mysql=true, spark=true
- `PORT_0022`: postgres=false, mysql=true, spark=true
- `PORT_0024`: postgres=false, mysql=true, spark=true
- `PORT_0025`: postgres=false, mysql=true, spark=true

Some target case IDs have MySQL or Spark SQLGlot optimize candidates, and several have no-op/reference candidates in unrelated roots. Those are not PostgreSQL SQLGlot optimize candidates and cannot fill the PG40 route row.

No naming difference such as `CASE_ID_postgres.sql` versus `CASE_ID__postgres.sql` explains the missing PostgreSQL files.
