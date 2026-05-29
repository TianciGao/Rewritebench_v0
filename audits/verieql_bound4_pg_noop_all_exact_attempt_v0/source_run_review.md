# Source Run Review

Source run: `runs/user/common_core_pg_noop_db_checker`

Baseline and engine:

- Method: SQLGlot noop
- Route: `noop`
- Engine: PostgreSQL

Source-run counts:

- Selected rows: 40
- Candidate generated rows: 40
- Source executable rows: 35
- Candidate executable rows: 35
- Checker success rows: 35
- Exact/result-consistent rows: 35
- Non-exact rows: 5

Exact rows by pool:

- PERF: 16
- CONS: 9
- PORT: 4
- LONGTAIL: 6

The 5 verifier-ineligible rows were:

- `PORT_0004`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

Those rows failed the exact/result-consistency gate because source-side execution failed in the source run. They were not sent to VeriEQL.
