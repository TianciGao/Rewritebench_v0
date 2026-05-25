# Protected Path Review

This task wrote committed artifacts only under `audits/nightly_user_reproduction_sqlglot_calcite_track_a_120_metrics_v0/` and project-control files.

Local diagnostic runtime outputs were written under `output/` and intentionally left uncommitted. The user-side source runs were created in a detached temporary worktree under `/tmp/sqlrb_nightly_user_repro_sqlglot_calcite_worktree`, so the current repository `runs/user/` tree was not modified.

Protected paths not modified or committed:

- `cases/`
- root-level `skills.md` files
- top-level `reports/`
- top-level `results/`
- case-local `runs/`
- current-repository `runs/user/` candidate roots
- retained evidence
- paper result files

No candidate SQL was moved, copied, or deleted from legacy `runs/user` roots. Fresh candidate SQL copies under `output/results/<run_id>/candidate_sql/` are local D035 user outputs and are not staged.
