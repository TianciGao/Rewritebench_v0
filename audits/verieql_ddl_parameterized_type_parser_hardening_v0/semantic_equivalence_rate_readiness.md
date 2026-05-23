# Semantic Equivalence Rate Readiness

This task did not compute Semantic Equivalence Rate.

Readiness update:
- The parameterized-DDL parser blocker identified by `verieql_one_baseline_feature_aware_subset_plan_v0` is fixed.
- The planned two-row subset, `CONS_0036` plus `CONS_0037`, is now ready for a separately authorized local-only exact-candidate VeriEQL pass.

Remaining boundaries:
- Any future local diagnostic rate must be named local/non-official.
- Decidable denominator remains `equivalent + non_equivalent`.
- `unsupported`, `not_implemented`, `timeout`, `unknown`, `syntax_error`, `out_of_memory`, `tool_error`, and `not_attempted` remain separately visible and excluded from the decidable denominator.
- Local result checker exactness remains an eligibility gate only, not verifier evidence.

