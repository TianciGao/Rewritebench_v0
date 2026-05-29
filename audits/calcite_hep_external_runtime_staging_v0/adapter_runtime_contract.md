# Adapter Runtime Contract

Adapter path:

- `baselines/calcite_hep_fail_closed/adapter.py`

External command shape:

```bash
<SQLRB_CALCITE_HEP_CMD> \
  --case-id <case_id> \
  --source-sql <source_sql_path> \
  --ddl <schema_ddl_path> \
  --output-sql <candidate_sql_path> \
  --mode <SQLRB_CALCITE_HEP_MODE>
```

If `SQLRB_CALCITE_HEP_CMD` is absent and `SQLRB_CALCITE_HEP_JAR` exists, the adapter uses:

```bash
<SQLRB_CALCITE_HEP_JAVA or java> -jar <SQLRB_CALCITE_HEP_JAR> ...
```

Schema resolution:

- The adapter resolves per-engine DDL from case-local `schema/ddl_<engine>.sql`, case-local `schema/<engine>/ddl.sql`, case-local schema profiles, or external schema profiles under `schemas/.../<engine>/ddl.sql`.
- The tiny smoke resolved:
  - `CONS_0036`: `schemas/verieql_cons0036_v0/postgres/ddl.sql`
  - `CONS_0037`: `schemas/verieql_cons0037_v0/postgres/ddl.sql`
  - `PERF_0006`: `schemas/tpch_common_core_v0/postgres/ddl.sql`

Status behavior:

- Runtime success with non-empty candidate file: `calcite_invocation_succeeded`.
- Missing runtime: `calcite_runtime_unavailable`.
- Missing Java: `calcite_java_missing`.
- Incomplete runtime configuration: `calcite_runtime_incomplete`.
- Missing schema DDL: `calcite_schema_unavailable`.
- Nonzero command exit: `calcite_invocation_failed`.
- Timeout: `calcite_invocation_timeout`.
- Zero exit with empty candidate file: `calcite_no_candidate_sql`.

Fail-closed rule:

The adapter exits `0` for route-level fail-closed conditions so the user-entry ledger records a normal adapter invocation with `no_candidate_sql` rather than an adapter crash. Only missing required adapter-runner environment variables remain adapter errors.
