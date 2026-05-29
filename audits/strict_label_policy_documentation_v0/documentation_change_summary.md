# Documentation Change Summary

## File Created

- `docs/user_entry_checker_policy.md`

## Rationale

No existing checker-policy document existed under `docs/`. The new file keeps the strict result-column label policy separate from broader user-entry how-to documentation.

## Policy Documented

- The local result checker is strict by default.
- Same-engine JSONL result column labels/object keys are part of exactness.
- Label-only mismatches remain mismatches.
- Diagnostic fields identify value-exact, label-different rows without changing outcomes.
- Explicit alias differences remain strict.
- Generated-expression labels are not automatically ignored.
- PORT real-adapter rows remain separate from controlled PORT target-reference diagnostics.
- Any exactness-changing label policy must be separately authorized and case/role/config gated.

## Non-Changes

- Checker behavior changed: no.
- Exact/mismatch semantics changed: no.
- Case-local label policy added: no.
- Global label-ignore behavior added: no.
- Common-core rerun performed: no.
- Official metrics, timing/speedup, reports/results, retained evidence, or leaderboard produced: no.
