# Command Log

All commands were run from `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`.

Initial checks:

```bash
pwd && git branch --show-current && git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
```

Read-only context:

```bash
find src/sql_rewrite_bench/pocr -maxdepth 2 -type f -print | sort
find tests/pocr -maxdepth 2 -type f -print | sort
find runs/user/common_core_pg_noop_db_checker -maxdepth 2 -type f | sort
python - <<'PY'
# Checked whether selected fixture cases had existing route-labeled candidate SQL artifacts.
PY
python - <<'PY'
# Checked live gate/provider env presence without printing values.
PY
```

Implementation edits:

```bash
apply_patch
```

Validation before live smoke:

```bash
python -m py_compile src/sql_rewrite_bench/pocr/__init__.py src/sql_rewrite_bench/pocr/annotation_client.py src/sql_rewrite_bench/pocr/live_smoke.py
pytest tests/pocr -q
```

Bounded live smoke:

```bash
python -m sql_rewrite_bench.pocr.live_smoke \
  --live-enabled \
  --case-list PERF_0006,CONS_0005,PORT_0003,LONGTAIL_0011 \
  --candidate-run-root runs/user/common_core_pg_noop_db_checker \
  --output-dir audits/pocr_live_api_annotation_smoke_v0 \
  --engine postgres \
  --method-id noop_adapter \
  --route-id common_core_pg_noop_db_checker
```

Post-smoke validation:

```bash
python -m py_compile src/sql_rewrite_bench/pocr/__init__.py src/sql_rewrite_bench/pocr/models.py src/sql_rewrite_bench/pocr/skills_parser.py src/sql_rewrite_bench/pocr/validation.py src/sql_rewrite_bench/pocr/inventory.py src/sql_rewrite_bench/pocr/annotation_schema.py src/sql_rewrite_bench/pocr/prompt_builder.py src/sql_rewrite_bench/pocr/annotation_client.py src/sql_rewrite_bench/pocr/evidence_validation.py src/sql_rewrite_bench/pocr/pocr_row.py src/sql_rewrite_bench/pocr/live_smoke.py
pytest tests/pocr -q
python - <<'PY'
# Parsed all 40 Common-core skills.md files and checked pool split/atom counts.
PY
python - <<'PY'
# CSV and JSONL parse checks for the audit packet.
PY
python - <<'PY'
# Markdown non-empty checks.
PY
git diff --check
git status -sb
git diff --name-status
```

No DB/checker/timing, baseline rerun, `compute-local-metrics`, verifier, official metrics, paper rendering, retained-evidence promotion, leaderboard, case package mutation, or user-output integration command was run.
