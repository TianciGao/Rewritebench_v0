# Command Log

Preflight and context commands:

```text
pwd && git branch --show-current && git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,120p' project_control/MIGRATION_STATUS.md
tail -n 140 project_control/DECISION_LOG.md
tail -n 140 project_control/MIGRATION_RUN_LOG.md
```

Validation commands:

```text
python CSV parse check for row_level_stage_b_schema.csv, required_columns.csv, and status_vocabulary.csv
find audits/pocr_row_level_stage_b_artifact_contract_v0 -name '*.md' -type f -print -exec test -s {} \;
python required boundary phrase check over audits/pocr_row_level_stage_b_artifact_contract_v0/*.md
git diff --check
git status --short --untracked-files=no cases case_sets inventory reports results runs/user output project_control audits/pocr_row_level_stage_b_artifact_contract_v0
git diff --name-only -- cases ':(glob)**/skills.md' case_sets inventory reports results runs/user output
git diff --name-only | rg '(^|/)candidate_sql/|\.sql$' || true
git diff -- project_control/DECISION_LOG.md project_control/MIGRATION_MASTER_PLAN.md
changed-file secret scan over project_control changes and audits/pocr_row_level_stage_b_artifact_contract_v0
```

Observed validation notes:

- CSV parse check succeeded for 39 schema rows, 39 required-column rows, and 15 status vocabulary rows.
- Required boundary phrases were found.
- `git diff --check` passed.
- No tracked protected-path diffs were present for `cases/`, `skills.md`, `case_sets/`, `inventory/`, top-level `reports/`, top-level `results/`, `runs/user`, `output/`, or candidate SQL paths.
- `project_control/DECISION_LOG.md` and `project_control/MIGRATION_MASTER_PLAN.md` were not modified.
- Pre-existing untracked `output/` and unrelated untracked artifacts remained untouched and uncommitted.

No experiment run, live API call, API key read, annotation JSONL generation, user replay rerun, DB/checker/timing run, baseline rerun, candidate SQL generation or mutation, official POCR computation, route-level official POCR score, paper-facing metric promotion, top-level reports/results update, retained-evidence promotion, or leaderboard output occurred.
