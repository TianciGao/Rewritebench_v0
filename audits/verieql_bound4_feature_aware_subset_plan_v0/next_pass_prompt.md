# Recommended Next Pass Prompt

Recommended next safe task:

`verieql_bound4_small_feature_aware_subset_pass_v0`

Goal:

Run a local-only, exact-gated VeriEQL finite-bound pass under one uniform declared policy over the proposed two-row feature-aware subset:

- `CONS_0036`
- `CONS_0037`

Verifier policy:

- `verifier_tool=verieql`
- `verifier_mode=finite_bound`
- `bound_size=4`
- `timeout_seconds=30`
- `cores=1`

Source run:

- `runs/user/common_core_pg_noop_db_checker`

Required boundaries:

- Do not run full Common-core.
- Do not run all exact rows through VeriEQL.
- Do not compute official Semantic Equivalence Rate.
- Do not update top-level `reports/` or `results/`.
- Do not promote retained evidence.
- Do not create leaderboard output.
- Do not mix bound sizes in one denominator.

Expected result:

- Confirm that the two already validated bound-4 rows remain clean all-`EQU` in a fresh small feature-aware pass.
- Keep the result local diagnostic only.
- Use the outcome to decide whether a later task should attempt a broader bound-4 subset after addressing LIKE, subquery, function/date-time, and dialect syntax blockers.
