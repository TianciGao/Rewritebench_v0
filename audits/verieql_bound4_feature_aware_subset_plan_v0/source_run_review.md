# Source Run Review

Source run: `runs/user/common_core_pg_noop_db_checker`

Baseline route and engine:

- Method: SQLGlot noop
- Route: `noop`
- Engine: PostgreSQL

Inventory result:

- Selected rows: 40
- Exact/result-consistent rows: 35
- Non-exact rows: 5

The five non-exact rows remain verifier-ineligible because they did not satisfy the exact/result-consistency gate in the source run:

- `PORT_0004`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

Exact rows by pool:

- PERF: 16
- CONS: 9
- PORT: 4
- LONGTAIL: 6

Only exact/result-consistent rows were reclassified for VeriEQL subset eligibility. Non-exact rows are excluded before verifier planning and should be labeled `not_exact_ineligible` in any execution task.
