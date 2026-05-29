# Command Log

## Preflight

```bash
git status -sb
git branch --show-current
git log --oneline -10
find /home/tianci_gao /mnt/data /tmp -iname '*Beyond*Faster*SQL*pdf' -o -iname 'Beyond_Faster_SQL*.pdf'
```

Starting state:

```text
## feature/case-package-v2-external-schema...origin/feature/case-package-v2-external-schema
branch: feature/case-package-v2-external-schema
latest commit: 2171f02 docs(decision): record metrics timing skill adapter deferral
```

PDF availability:

```text
No local Beyond_Faster_SQL PDF was found under /home/tianci_gao, /mnt/data, or /tmp.
```

## Required Context Reads

```bash
sed -n '1,240p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,260p' project_control/MIGRATION_STATUS.md
tail -n 260 project_control/MIGRATION_RUN_LOG.md
sed -n '1,860p' project_control/DECISION_LOG.md
sed -n '1,260p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
sed -n '1,340p' repository_spec/metrics_contract_v1.md
sed -n '1,320p' repository_spec/metrics_contract_v1_draft.md
sed -n '1,200p' repository_spec/explainability_attribution_policy_v1_draft.md
find audits/metrics_timing_skill_adapter_decision_record_v0 -maxdepth 1 -type f -print -exec sed -n '1,220p' {} \;
sed -n '1,140p' docs/user_entry_checker_policy.md
sed -n '1,160p' audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/README.md
sed -n '1,160p' audits/checker_label_only_diagnostics_patch_v0/README.md
```

## Validation

Validation commands were run after audit and project-control writeback; see `protected_surface_check.md`.
