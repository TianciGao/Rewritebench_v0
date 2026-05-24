# Adapter Mode Contract

Adapter path:

`baselines/calcite_hep_fail_closed/adapter.py`

The adapter now passes the target engine to the runtime:

```text
--engine postgres|mysql|spark
```

The value is derived from the user-run `SQLRB_ENGINE` environment value, with
`pg` normalized to `postgres`.

The runtime command shape is now:

```text
calcite-hep-rewrite-smoke \
  --case-id <case_id> \
  --source-sql <source-sql> \
  --ddl <schema-ddl> \
  --output-sql <candidate-sql> \
  --mode real_route_canary \
  --engine <target-engine>
```

Compatibility behavior:

- Older runtimes that ignore `--engine` can still run.
- If they emit PostgreSQL-dialect SQL for MySQL/Spark, the existing adapter
  fail-closed guard blocks the candidate before DB execution.
- Runtimes that support `--engine` should emit target-dialect SQL.

Traceability added:

- `runtime.target_engine` is recorded in `calcite_hep_status.json`.
- `runtime_target_engine` is recorded in the top-level status payload.

The adapter still does not rewrite case SQL and does not implement a broad SQL
dialect converter.
