# verieql_cons0037_bound_timeout_policy_probe_v0

Targeted local-only VeriEQL finite-bound bound/timeout policy probe for the `CONS_0037` SQLGlot-noop PostgreSQL exact candidate row from `runs/user/common_core_pg_noop_db_checker`.

Verdict:
- `CONS_0037` was exact-gated again.
- `bound_size` 1, 2, 3, and 4 at 30 seconds returned clean all-`EQU` and normalized to `equivalent`.
- `bound_size` 5 and 10 timed out at 30 seconds.
- Retrying `bound_size` 5 and 10 at 120 seconds did not change the result; both remained `timeout`.
- No 300-second run was performed because 120 seconds did not produce a clean or otherwise policy-changing result.

Policy conclusion:
- `CONS_0037` is cleanly bounded-equivalent only at smaller declared bounds through 4.
- `CONS_0037` is not feasible at `bound_size=10` under the tested timeout settings.
- Do not mix bound sizes inside one Semantic Equivalence Rate denominator without a separate durable policy.
- A next small feature-aware subset can include `CONS_0037` only if the pass declares a uniform smaller bound, such as `bound_size=4`, and reports that bound explicitly.
- Full Common-core exact-candidate verifier pass remains blocked.

This is local verifier-support probing only. It is not official Semantic Equivalence Rate, not a Common-core pass, not paper evidence, not retained evidence, and not leaderboard input.

