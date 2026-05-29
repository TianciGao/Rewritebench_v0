# Source Audits

Input route-card audits:

1. `audits/sqlglot_noop_pg_current_route_card_refresh_v0/`
   - `route_card.json`
   - `route_card.csv`
   - `non_exact_frontier.md`
2. `audits/calcite_hep_pg_post_quoting_chain_rerun_v0/`
   - `route_card.json`
   - `route_card.csv`
   - `non_exact_frontier.md`

Preflight confirmed both input audit packets and both `route_card.json` /
`route_card.csv` files exist.

Commit ancestry confirmed:

- SQLGlot noop PG refresh commit `35a97d620eee82cdd0235bb941f9ee4b3a8c47bf` is an ancestor of this branch.
- Calcite PG post-quoting rerun commit `b261ee0bde85856ae57bc4e310eadb0fcbdc6cf2` is an ancestor of this branch.

This packet uses existing route-card outputs only. It does not rerun either
route.
