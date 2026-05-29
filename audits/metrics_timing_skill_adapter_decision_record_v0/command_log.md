# Command Log

## Preflight

```bash
git status -sb
git branch --show-current
git log --oneline -10
find .. . -maxdepth 4 -iname '*Beyond*Faster*SQL*pdf' -o -iname 'Beyond_Faster_SQL*.pdf'
find /home/tianci_gao -iname '*Beyond*Faster*SQL*pdf' -o -iname 'Beyond_Faster_SQL*.pdf'
```

Starting state:

```text
## feature/case-package-v2-external-schema...origin/feature/case-package-v2-external-schema
branch: feature/case-package-v2-external-schema
latest commit: a974c46 docs(user-entry): document strict checker label policy
```

PDF availability:

```text
No local Beyond_Faster_SQL PDF was found under /home/tianci_gao.
```

## Required Context Reads

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,260p' project_control/MIGRATION_STATUS.md
tail -n 220 project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' project_control/DECISION_LOG.md
sed -n '350,820p' project_control/DECISION_LOG.md
sed -n '1,260p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
sed -n '1,140p' docs/user_entry_checker_policy.md
sed -n '1,180p' audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0/README.md
sed -n '1,140p' audits/checker_label_only_diagnostics_patch_v0/README.md
sed -n '1,340p' repository_spec/metrics_contract_v1.md
sed -n '1,180p' repository_spec/explainability_attribution_policy_v1_draft.md
```

## Inspection Commands

```bash
rg -n "^## D[0-9]+|metrics|Metric|Attribution|Speedup|Operation|POCR|Positive Operation" project_control/DECISION_LOG.md repository_spec/metrics_contract_v1.md repository_spec/explainability_attribution_policy_v1_draft.md
rg --files repository_spec | sort
```

## Validation

Validation commands were run after audit and project-control writeback; see `protected_surface_check.md`.
