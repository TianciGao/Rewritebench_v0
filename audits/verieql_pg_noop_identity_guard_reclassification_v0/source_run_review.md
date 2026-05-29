# Source Run Review

Source run: `runs/user/common_core_pg_noop_db_checker`

Method/route/engine:

- Method: SQLGlot noop
- Route: `noop`
- Engine: PostgreSQL

Prior all-exact attempt:

- `audits/verieql_bound4_pg_noop_all_exact_attempt_v0/`

Source run counts:

- Selected rows: 40
- Exact/result-consistent rows: 35
- Prior source-vs-candidate VeriEQL attempted rows: 35
- Non-exact verifier-ineligible rows: 5

The 5 non-exact rows were not identity-checked and remain `not_checked_not_exact_ineligible`:

- `PORT_0004`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

Runtime output for identity checks was written only under:

- `/tmp/sqlrb_verieql_pg_noop_identity_guard_reclassification_v0/`
