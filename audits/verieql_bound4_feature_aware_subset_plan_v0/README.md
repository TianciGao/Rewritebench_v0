# verieql_bound4_feature_aware_subset_plan_v0

Task mode: planning/audit only.

Branch: `feature/case-package-v2-external-schema`

Source run inspected: `runs/user/common_core_pg_noop_db_checker`

Uniform verifier policy planned for the next pass:

- `verifier_tool=verieql`
- `verifier_mode=finite_bound`
- `bound_size=4`
- `timeout_seconds=30`
- `cores=1`

Verdict: ready for a small bound-4 feature-aware exact-candidate pass over the two already validated rows, `CONS_0036` and `CONS_0037`. The refreshed inventory did not identify an additional low-risk exact row for the first expansion. Rows with `LIKE`, `EXISTS` or nested subqueries, date/time or function-heavy logic, and dialect syntax risks remain blocked from the first bound-4 expansion.

Counts:

- Selected rows in source run: 40
- Exact/result-consistent rows: 35
- Non-exact verifier-ineligible rows: 5
- Already validated bound-4 equivalent rows: 2
- Proposed next subset rows: 2

This packet does not run VeriEQL over the proposed subset, compute official Semantic Equivalence Rate, update top-level `reports/` or `results/`, promote retained evidence, or create leaderboard output.

Created artifacts:

- `source_run_review.md`
- `exact_row_inventory.md`
- `exact_row_inventory.csv`
- `updated_feature_eligibility_review.md`
- `updated_feature_eligibility_matrix.csv`
- `bound4_policy.md`
- `proposed_bound4_subset.md`
- `proposed_bound4_subset.csv`
- `semantic_equivalence_denominator_policy.md`
- `next_pass_prompt.md`
- `command_log.md`
- `protected_surface_check.md`
- `boundary_checklist.md`
