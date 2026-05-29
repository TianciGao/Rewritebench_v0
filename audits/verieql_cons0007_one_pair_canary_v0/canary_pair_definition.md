# Canary Pair Definition

Run id:

```text
verieql_cons0007_one_pair_canary_v0
```

Pair id:

```text
CONS_0007_source_vs_positive_pos_01
```

Pair type:

```text
source_vs_positive
```

Files:

```text
source_sql_path=cases/CONS/CONS_0007/sql/source.sql
positive_sql_path=cases/CONS/CONS_0007/sql/pos_01.sql
schema_context_path=schemas/calcite_core_sql_tests_cons0007_v0/postgres/ddl.sql
checker_context_path=cases/CONS/CONS_0007/checker/checker.yaml
```

Manifest basis:

- `cases/CONS/CONS_0007/manifest.yaml` declares `sql/source.sql`.
- `cases/CONS/CONS_0007/manifest.yaml` declares positive rewrite `pos_01` at `sql/pos_01.sql`.
- `cases/CONS/CONS_0007/manifest.yaml` declares external schema profile `schemas/calcite_core_sql_tests_cons0007_v0/schema_profile.yaml`.
- The wrapper accepts SQL/JSON schema contexts; the canary used the PostgreSQL DDL path from the external schema profile.

Expected high-level intent:

- The positive rewrite is expected to preserve the source semantics.
- The canary did not force an expected verdict. It recorded the tool output as observed.

Boundary flags:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`
