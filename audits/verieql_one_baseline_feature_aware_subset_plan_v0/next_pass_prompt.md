# Next Pass Prompt

Suggested next task title:
- `verieql_bounded_one_baseline_exact_subset_v0`

Suggested scope:
- Harden DDL parsing for parameterized types in the VeriEQL wrapper.
- Run exactly the planned subset:
  - `CONS_0036`
  - `CONS_0037`
- Use source run `runs/user/common_core_pg_noop_db_checker`.
- Use route/method `sqlglot_noop`.
- Use engine `postgres`.
- Use `verifier_mode=finite_bound`, `bound_size=10`, `timeout_seconds=30`, `cores=1`.
- Do not run all exact rows.
- Do not compute official Semantic Equivalence Rate.
- Do not update top-level `reports/` or `results/`.
- Do not promote retained evidence.
- Do not create leaderboard output.

Required outputs:
- Local-only verifier summary over the two attempted rows.
- Per-row verdict table.
- Explicit `verifier_eligibility_rate`, `verifier_decidability_rate`, and local diagnostic semantic equivalence rate over decidable rows only.
- Explicit list of rows excluded by feature-aware eligibility.

Stop conditions:
- If DDL parser hardening is not implemented, do not expand beyond `CONS_0036`.
- If `CONS_0037` returns `NIE`, `NSE`, `TMO`, `UNK`, `SYN`, `OOM`, or `OTE`, keep it visible and excluded from the decidable denominator.

