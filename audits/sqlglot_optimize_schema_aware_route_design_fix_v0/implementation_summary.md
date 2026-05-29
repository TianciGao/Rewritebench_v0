# Implementation Summary

Files changed:
- `baselines/sqlglot/sqlglot_user_adapter.py`
- `baselines/sqlglot/README.md`
- `tests/user_entry/test_sqlglot_adapter.py`
- `tests/user_entry/test_local_timing.py`

Adapter changes:
- Added route id mapping for `optimize_schema_aware`.
- Added DDL/schema resolution helpers in the SQLGlot baseline adapter.
- Added DDL-to-SQLGlot schema map extraction.
- Added schema-aware optimize generation.
- Added per-row adapter status JSON.
- Kept `noop` and context-free `optimize` behavior available.

Test changes:
- Added route identity coverage for `sqlglot_optimize_schema_aware`.
- Added DDL schema extraction coverage.
- Added missing-schema fail-closed coverage.
- Added `CONS_0005` invalid qualification regression coverage.
- Added user-entry candidate ledger smoke for the schema-aware route.

No route-specific SQLGlot logic was added under `src/sql_rewrite_bench/`.
