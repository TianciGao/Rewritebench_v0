# ci_user_entry_smoke_checkout_failure_probe_v0

Audit-only probe for the GitHub Actions `user-entry-smoke` checkout failure on commit `0c53cc7d492bc14cf4bf9d97506ce86e002b4976`.

Verdict: the observed failure did not reproduce locally and is not supported by the repository workflow configuration as a benchmark-code regression. The failed run was `user-entry-smoke` run `#453` for the `push` event. It failed at `Checkout repository` before Python setup or tests. A sibling `Ledger fixture smoke` push run on the same commit succeeded, and a subsequent `user-entry-smoke` pull-request run on the same commit also succeeded end to end.

No workflow file was changed. The strongest classification is GitHub checkout/auth/run-context transient or GitHub-side token/remote credential failure, not VeriEQL DDL parser hardening.

Files in this packet:
- `workflow_comparison.md`
- `github_run_context.md`
- `local_validation_results.md`
- `protected_surface_check.md`
- `command_log.md`
- `boundary_checklist.md`

