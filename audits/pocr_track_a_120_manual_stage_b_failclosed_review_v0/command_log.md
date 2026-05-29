# Command Log

Metric-definition checkpoint:
- POCR@planned and POCR@candidate remain D039 promotion views.
- POCR@curated remains NA / curated_manifest_missing until a predeclared curated manifest exists.
- Macro-average over per-row OC_i is the formula.
- Diagnostic micro-average is not the paper formula.
- Expected atoms come only from operation_atom entries in case-local root-level skills.md.
- semantic_guard_atom is excluded from numerator and denominator.
- Implemented atoms come only from Stage-B transformation-supported operation atoms.
- Stage A annotation alone is not counted.
- candidate/source/positive span presence alone is not enough.
- source-to-candidate transformation evidence is required.
- SQLGlot no-op remains a candidate/control route, not a reference.
- positive SQL is reference evidence, not an atom source.

Commands run:
- `pwd`
- `git branch --show-current`
- `git status -sb --untracked-files=normal`
- `sed -n` / `tail` reads of `project_control/MIGRATION_MASTER_PLAN.md`, `project_control/MIGRATION_STATUS.md`, `project_control/DECISION_LOG.md`, and `project_control/MIGRATION_RUN_LOG.md`
- `find audits/... -maxdepth 1 -type f | sort` for required prior audit packets
- `find tests/pocr -maxdepth 2 -type f | sort`
- `sed -n` reads of `src/sql_rewrite_bench/pocr/stage_b_row_metrics.py`, `src/sql_rewrite_bench/pocr/pocr_aggregator.py`, and `src/sql_rewrite_bench/pocr/operation_evidence_policy.py`
- Python read-only inspection of final retry row metrics, replay manifests, aggregate summaries, and safe annotation JSONL for the isolated route-mismatch row
- Python generation of this audit packet from existing row metrics and audit artifacts

No live API call was made. No API key was read. No retry, annotation generation, pocr-diagnostic replay rerun, POCR aggregation rerun, DB/checker/timing run, baseline rerun, candidate generation, or candidate mutation occurred.

Validation commands are appended in `validation_summary.md` after validation completes.

Validation commands run:
- `python -m py_compile src/sql_rewrite_bench/pocr/stage_b_row_metrics.py src/sql_rewrite_bench/pocr/pocr_aggregator.py src/sql_rewrite_bench/pocr/operation_evidence_policy.py`
- CSV parse and Markdown required phrase checks for `audits/pocr_track_a_120_manual_stage_b_failclosed_review_v0/`
- `git diff --check`
- `pytest tests/pocr -q`
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q`
- `git diff --name-status`
- protected-path checks for `cases/`, `skills.md`, candidate SQL, `runs/user`, `output/`, `/tmp`, top-level `reports/`, and top-level `results/`
