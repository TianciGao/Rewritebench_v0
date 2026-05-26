# Command Log

Initial checks:

```bash
pwd
git branch --show-current
git status -sb --untracked-files=normal
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,260p' project_control/DECISION_LOG.md
sed -n '1,220p' project_control/MIGRATION_RUN_LOG.md
```

Context and artifact reads:

```bash
find audits -maxdepth 2 -type f ...
find output/results -path '*pocr*' -name safe_annotation_outputs.jsonl -o -name merged_safe_annotation_outputs.jsonl -o -name pocr_stage_b_row_metrics.csv -o -name pocr_route_summary.csv
python scripts used read-only CSV/JSONL parsing of prior pilot audit packets and local D035 output artifacts
```

Live retry preflight:

- Provider label and model label were read from supported POCR/LLM configuration metadata.
- API key presence was checked from the configured environment variable name only; no API key value was printed or written.
- Explicit live gate was present.

Retry/replay/aggregation commands used existing Python entry points and modules:

```bash
python -m sql_rewrite_bench.pocr.checkpointed_annotation_runner ... --allow-live --retry-failed --case-id <selected fail-closed cases>
python -m cli.main user pocr-diagnostic --enable-pocr-diagnostic --candidate-root <selected root> --annotation-jsonl <merged jsonl> --method-id <method> --route-id <route> --engine <engine> --run-id <retry replay run id> --output-root output
python aggregator helper over the six retry replay pocr_stage_b_row_metrics.csv files into output/results/pocr_aggregate_tri_engine_pilot_retry_merged_v0/pocr/aggregates/pocr_route_summary.csv
```

Results captured:

- Retry live calls attempted: 9
- Retry schema-valid rows: 1
- Remaining fail-closed rows after replay: 8
- Replay rows emitted: 30
- Route mismatch rows: 0
- Candidate mismatch rows: 0
- Aggregation rerun completed: yes

Validation commands:

```bash
python - <<'PY'
# CSV, JSONL, row-metrics, aggregate, Markdown, and required phrase checks
PY
python -m py_compile src/sql_rewrite_bench/pocr/stage_b_row_metrics.py src/sql_rewrite_bench/pocr/pocr_aggregator.py src/sql_rewrite_bench/pocr/checkpointed_annotation_runner.py
pytest tests/pocr -q
pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
git diff --check
git status --short cases case_sets inventory reports results runs/user output
git diff --name-status -- cases case_sets inventory reports results runs/user project_control audits src tests
git status -sb --untracked-files=normal
```

Validation results before staging:

- CSV, JSONL, row-metrics, aggregate, Markdown, and required phrase checks passed.
- `pytest tests/pocr -q`: 143 passed.
- User-entry tests: 28 passed.
- `git diff --check`: passed.
- Protected path check found no `cases/`, `skills.md`, candidate SQL, `runs/user`, top-level `reports/`, or top-level `results` modifications. Local `output/` remains untracked and is not staged.
- Changed-file secret scan passed for the new audit packet and modified project-control files.
- Staged secret scan passed after selective staging.
