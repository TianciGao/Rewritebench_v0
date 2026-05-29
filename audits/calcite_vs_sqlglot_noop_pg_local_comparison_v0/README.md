# calcite_vs_sqlglot_noop_pg_local_comparison_v0

Date: 2026-05-24

Mode: bounded local-only PostgreSQL comparison audit.

This packet compares existing refreshed route-card audits only:

- `audits/sqlglot_noop_pg_current_route_card_refresh_v0/`
- `audits/calcite_hep_pg_post_quoting_chain_rerun_v0/`

No SQLGlot rerun, Calcite rerun, SQL execution, timing collection, verifier
pass, official metric computation, paper update, retained-evidence promotion,
leaderboard output, denominator change, or case membership change occurred.

## Summary

| route | selected | generated | candidate executable | exact | timed exact | diagnostic GM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SQLGlot noop | 40 | 35 | 35 | 35 | 35 | 0.995912 |
| Calcite HEP fail-closed | 40 | 33 | 28 | 22 | 22 | 1.009852 |

Safe interpretation:

- SQLGlot noop has higher PostgreSQL exact coverage in this local diagnostic run: 35/40 vs Calcite HEP 22/40.
- Calcite HEP has slightly above-parity diagnostic GM speedup over its own 22 exact-timed rows.
- SQLGlot noop is a low-transform infrastructure/control route, not an optimizer-strength claim.
- Calcite HEP exposes route-development frontier: no-candidate rows, schema-fallback exclusions, a source-role failure, and mismatches.
- This is a bounded local PostgreSQL diagnostic comparison only.
