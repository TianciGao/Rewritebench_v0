# Next Bounded PostgreSQL Run Plan

The route is ready for a separately authorized bounded PostgreSQL-only local diagnostic run.

Recommended next scope:

- Engine: PostgreSQL only.
- Route: `calcite_hep_fail_closed`.
- Runtime env:
  - `SQLRB_CALCITE_HEP_CMD=/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke`
  - `SQLRB_CALCITE_HEP_ROOT=/home/tianci_gao/.local/share/sqlrb/calcite_hep`
  - `SQLRB_CALCITE_HEP_JAVA=/usr/bin/java`
  - `SQLRB_CALCITE_HEP_TIMEOUT=30`
- Start with a bounded subset before Common-core expansion.
- Enable database execution/checker only in a separate task if the generated candidates are reviewed and the scope is explicit.

Blocked before tri-engine or full 120:

- MySQL/Spark Calcite SQL rendering and schema compatibility are not validated in this release path.
- No execution/checker closure has been established for the generated candidates.
- No timing/speedup route has been authorized.
- Direct LLM and Repair-1 remain deferred until deterministic route behavior is stable.
