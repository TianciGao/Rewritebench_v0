# Selection Review

Preferred rows were selected exactly as requested:

| Case ID | Pool | Rationale |
|---|---|---|
| `CONS_0036` | CONS | VeriEQL identity-passed equivalent row. |
| `CONS_0037` | CONS | VeriEQL identity-passed equivalent row after DDL hardening and bound-4 policy. |
| `LONGTAIL_0023` | LONGTAIL | VeriEQL identity/modeling failure despite byte-identical source/candidate. |
| `PORT_0003` | PORT | VeriEQL identity-passed equivalent row; non-CONS coverage. |
| `PORT_0005` | PORT | VeriEQL identity-passed equivalent row; non-CONS coverage. |

No fallback rows were needed.

The source run was `runs/user/common_core_pg_noop_db_checker`, route/method was SQLGlot noop, and engine was PostgreSQL.
