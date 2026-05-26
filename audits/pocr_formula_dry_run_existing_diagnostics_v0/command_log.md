# Command Log

Preflight and context commands:

```text
pwd && git branch --show-current && git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,160p' project_control/MIGRATION_STATUS.md
tail -n 140 project_control/DECISION_LOG.md
tail -n 140 project_control/MIGRATION_RUN_LOG.md
find audits/pocr_step5_repair1_pg40_targeted_retry_v0 audits/pocr_repair1_exemplar_closeout_and_sqlglot_optimize_pg40_start_v0 audits/pocr_sqlglot_noop_pg40_sanity_control_v0 -maxdepth 1 -type f | sort
find output/results -path '*pocr*' -maxdepth 8 -type f 2>/dev/null | sort
find /tmp/sqlrb_pocr_user_replay_direct_llm_repair1_pg40_targeted_retry_v0 /tmp/sqlrb_pocr_user_replay_sqlglot_noop_pg40_sanity_control_v0 -maxdepth 8 -type f 2>/dev/null | sort
head -n 3 /tmp/sqlrb_pocr_user_replay_direct_llm_repair1_pg40_targeted_retry_v0/output/results/pocr_user_replay_direct_llm_repair1_pg40_targeted_retry_v0/pocr/diagnostic_rows.csv
head -n 3 /tmp/sqlrb_pocr_user_replay_sqlglot_noop_pg40_sanity_control_v0/output/results/pocr_user_replay_sqlglot_noop_pg40_sanity_control_v0/pocr/diagnostic_rows.csv
```

Generation command:

```text
python script generated this audit from existing diagnostic CSV/JSONL files only.
```

Validation commands:

```text
python CSV parse check over audits/pocr_formula_dry_run_existing_diagnostics_v0/*.csv
find audits/pocr_formula_dry_run_existing_diagnostics_v0 -name '*.md' -type f -print -exec test -s {} \;
rg required boundary phrases in audits/pocr_formula_dry_run_existing_diagnostics_v0
git diff --check
git status --short -- output
git status --short -- cases ':(glob)**/skills.md' runs/user reports results
git diff --name-only -- cases ':(glob)**/skills.md' runs/user reports results output
git diff --name-only | rg '(^|/)candidate_sql/|\.sql$' || true
```

No live API call, API key read, annotation JSONL generation, user replay rerun, DB/checker/timing run, baseline rerun, candidate SQL generation or mutation, official POCR computation, paper-facing metric promotion, top-level reports/results update, retained-evidence promotion, or leaderboard output was run.

Observed validation summary:

- CSV parse checks passed for all audit CSV files.
- Markdown non-empty checks passed for all audit Markdown files.
- Required boundary phrase checks passed.
- `git diff --check` passed.
- Protected-path checks found no tracked changes under `cases/`, `skills.md`, `runs/user`, top-level `reports/`, top-level `results`, or candidate SQL paths.
- Local `output/` remains untracked and was not staged.
