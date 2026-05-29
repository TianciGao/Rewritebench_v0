# strict_label_policy_documentation_v0

Verdict: `completed`

This documentation-only task records the current strict result-column label policy for user-entry local diagnostics after `checker_label_only_diagnostics_patch_v0`.

## Summary

- Created `docs/user_entry_checker_policy.md`.
- Documented that same-engine local checker comparisons are strict by default and treat JSONL object keys/result column labels as part of exactness.
- Documented that label-only mismatches remain `checker_mismatch`, `exact_status=mismatch`, and `failure_bucket=mismatch`.
- Documented the diagnostic fields added by the prior behavior-preserving patch.
- Documented that `label_only_mismatch=true` is visibility only, not a correctness relaxation.
- Documented that explicit aliases remain strict and generated-expression labels are not automatically ignored.
- Documented that PORT real-adapter rows remain separate from controlled PORT target-reference diagnostics.
- Documented that any exactness-changing label policy requires separate authorization and explicit case/role/config gating.

No checker behavior, exact/mismatch semantics, case packages, SQL, checker configs, baselines, `case_sets/`, reports/results, retained evidence, official metrics, timing/speedup, or leaderboard outputs changed.

## Next Safe Action

Keep label-only rows fail-visible under the documented strict policy unless a separate task authorizes a case- or role-gated exactness-changing label policy.
