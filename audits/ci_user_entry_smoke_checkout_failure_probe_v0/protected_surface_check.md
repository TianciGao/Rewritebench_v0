# Protected Surface Check

Allowed changed paths for this audit:
- `audits/ci_user_entry_smoke_checkout_failure_probe_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `.github/workflows/user_entry_smoke.yml` only if a root-cause workflow fix was confirmed

Actual workflow change:
- `.github/workflows/user_entry_smoke.yml` was not changed.

Protected paths:
- `src/`: unchanged.
- `tests/`: unchanged.
- `scripts/`: unchanged.
- `cases/`: unchanged.
- `case_sets/`: unchanged.
- `baselines/`: unchanged.
- `reports/`: unchanged.
- `results/`: unchanged.
- repository-level `output/`: unchanged.
- `runs/user/`: no committed output.

Runtime/generated cleanup:
- `src/sql_rewrite_bench.egg-info/` from editable install was removed.
- A validation refresh under `audits/ledger_fixture_dev_smoke/` was restored and not committed.

Conclusion:
- Protected-surface check passed for this audit-only probe.

