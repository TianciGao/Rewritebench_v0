# Evidence Chain Summary

Relevant audit chain:

- `verieql_finite_bound_wrapper_mode_v0`: implemented finite-bound mode, schema identifier canonicalization, and strict state normalization.
- `verieql_exact_candidate_tiny_local_pass_v0`: proved the wrapper can reach real exact candidate rows.
- `verieql_one_baseline_feature_aware_subset_plan_v0`: identified early feature blockers and DDL parser gaps.
- `verieql_ddl_parameterized_type_parser_hardening_v0`: hardened parameterized DDL type parsing.
- `verieql_cons0036_cons0037_two_row_exact_candidate_pass_v0`: showed `CONS_0036` equivalent and `CONS_0037` timeout at bound 10.
- `verieql_cons0037_bound_timeout_policy_probe_v0`: showed `CONS_0037` is clean at bounds 1 through 4 and timeout-prone at 5 and 10.
- `verieql_bound4_two_row_uniform_policy_pass_v0`: showed `CONS_0036` and `CONS_0037` both clean all-`EQU` under bound 4.
- `verieql_bound4_feature_aware_subset_plan_v0`: refreshed the feature-aware subset plan under bound 4.
- `verieql_bound4_pg_noop_all_exact_attempt_v0`: attempted all 35 exact SQLGlot-noop PostgreSQL rows under bound 4.
- `verieql_longtail0023_non_equivalent_triage_v0`: triaged `LONGTAIL_0023` as a VeriEQL identity/modeling diagnostic, not candidate drift.
- `verieql_pg_noop_identity_guard_reclassification_v0`: applied identity guard and corrected the local diagnostic denominator.

Technical closeout:

- Timeout mode is unsuitable for clean equivalence when raw states include `EQU...TMO`; those rows must remain timeout.
- Finite-bound mode works and is the usable VeriEQL path.
- Schema uppercase canonicalization is required.
- Parameterized DDL types such as `VARCHAR(32)` are preserved after parser hardening.
- Bound 4 with 30 seconds and one core is the only current uniform policy that supports the validated two-row path including `CONS_0037`.
