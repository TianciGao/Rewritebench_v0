# Command Log

## Preflight

- `git status -sb`: clean worktree.
- `git branch --show-current`: `feature/case-package-v2-external-schema`.
- `git log --oneline -12`: reviewed latest branch history through user-entry U0-U7 closeout.

## Context Reads

- Read project-control master plan, status, decision log, run-log tail, and user-entry architecture plan.
- Read user-entry local evaluation phase closeout packet.
- Inventoried top-level release-surface files and directories.
- Inspected README, docs, workflows, repository specs, case-set counts, Common-core case package surface, and local output policy.

## Findings

- Common-core v0 case count: 40.
- Pool split: 16 PERF + 9 CONS + 9 PORT + 6 LONGTAIL.
- Track A same-engine denominator rows: 120.
- Missing public metadata: `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`, `benchmark_spec/`, `reports/`, `results/`, and root `.gitignore`.
- User-entry U0-U7 can be treated as completed with deferred items.
- Timing, official metrics, paper reproduction, reports/results migration, release export/tagging, and global leaderboard remain deferred and unauthorized.

## Validation

- `git diff --check`: passed.
- CSV parse checks for new CSV files: passed.
- Markdown sanity checks for new Markdown files: passed.
- Protected-surface diff check: passed.
- No `runs/user/` outputs created.
