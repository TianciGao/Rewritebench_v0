# Decision Traceability

## Evidence Source

The immediate evidence source is `audits/user_entry_port_pg_source_failure_triage_v0/`.

That triage showed:

- five PORT failures reproduced under PostgreSQL local diagnostics;
- all five failures occurred during source query execution;
- all five retained `sql/source.sql` files are MySQL-like source SQL;
- no target case has a PostgreSQL dialect variant under `sql/dialect_variants/postgres/`;
- `pos_01.sql` appears PostgreSQL-like but is declared as a positive rewrite, not a PostgreSQL source oracle.

## Decision Recorded

D031 records that PORT cross-dialect diagnostics require explicit manifest roles and fail-closed runner behavior.

The decision requires:

- manifest-declared PORT cross-dialect diagnostic roles;
- no role inference from file names;
- no role inference from SQL text;
- no automatic `pos_01.sql` source-oracle substitution;
- same-engine behavior as the default for cases without cross-dialect metadata;
- MySQL source-side execution before these MySQL-like PORT diagnostics can be completed;
- Spark deferred unless separately authorized.

## Protected Boundaries

D031 does not authorize:

- source code implementation;
- manifest edits;
- SQL edits;
- MySQL or Spark live execution;
- official metrics;
- timing/speedup;
- paper table rendering;
- reports/results updates;
- retained-evidence promotion;
- denominator changes;
- paper-result changes;
- case membership changes;
- raw legacy evidence changes;
- global leaderboard output.
