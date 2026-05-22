# Command Log

## Preflight

```bash
git status -sb
git branch --show-current
git log --oneline -8
rg --files docs project_control audits/mysql_label_policy_triage_v0 audits/checker_label_policy_design_v0 audits/checker_label_only_diagnostics_patch_v0
```

Starting state:

```text
## feature/case-package-v2-external-schema...origin/feature/case-package-v2-external-schema
branch: feature/case-package-v2-external-schema
latest commit: 4dbd050 fix(checker): add label-only mismatch diagnostics
```

## Required Context Reads

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,260p' project_control/MIGRATION_STATUS.md
tail -n 220 project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' project_control/DECISION_LOG.md
sed -n '1,260p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
```

```bash
for f in audits/mysql_label_policy_triage_v0/*.md audits/checker_label_policy_design_v0/*.md audits/checker_label_only_diagnostics_patch_v0/*.md; do
  printf '\n## %s\n' "$f"
  sed -n '1,220p' "$f"
done
```

```bash
sed -n '1,240p' docs/USER_ENTRY_DATA_FLOW.md
sed -n '1,220p' docs/USER_BENCHMARK_GUIDE.md
sed -n '1,160p' docs/README.md
```

## Validation

Validation commands were run after documentation and project-control writeback; see `protected_surface_check.md`.
