# Command Log

All commands were run from `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`.

## Pre-edit Checks

```bash
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
```

## Read-only Inspection

```bash
rg --files src/sql_rewrite_bench/pocr
rg --files tests/pocr
find audits/pocr_live_api_annotation_smoke_v0 -maxdepth 1 -type f -printf '%f\n' | sort
find audits/pocr_candidate_resolver_draft_runner_v0 -maxdepth 1 -type f -printf '%f\n' | sort
head -n 5 audits/pocr_live_api_annotation_smoke_v0/safe_annotation_outputs.jsonl
sed -n '1,260p' src/sql_rewrite_bench/pocr/annotation_schema.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/evidence_validation.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/candidate_resolver.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/draft_runner.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/models.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/inventory.py
sed -n '1,220p' src/sql_rewrite_bench/pocr/json_output_guard.py
sed -n '1,220p' src/sql_rewrite_bench/pocr/__init__.py
sed -n '1,260p' tests/pocr/test_draft_runner.py
sed -n '1,260p' tests/pocr/test_candidate_resolver.py
sed -n '1,280p' tests/pocr/test_evidence_validation.py
sed -n '1,220p' tests/pocr/test_annotation_schema.py
```

## Implementation and Diagnostic Dry-run

Manual source/test edits were made with `apply_patch`.

```bash
python -m py_compile src/sql_rewrite_bench/pocr/annotation_resolver.py src/sql_rewrite_bench/pocr/static_evidence.py src/sql_rewrite_bench/pocr/stage_b_static_runner.py src/sql_rewrite_bench/pocr/__init__.py
pytest tests/pocr -q
python - <<'PY'
# Generated audit-only CSV/Markdown outputs under audits/pocr_stage_b_static_evidence_validator_v0/.
# The script resolved existing candidates and prior annotation artifacts read-only.
PY
find audits/pocr_stage_b_static_evidence_validator_v0 -maxdepth 1 -type f -printf '%f\n' | sort
```

## Validation

```bash
python -m py_compile $(rg --files src/sql_rewrite_bench/pocr -g '*.py')
pytest tests/pocr -q
python - <<'PY'
# Parsed all 40 Common-core skills.md files, resolved the bounded candidate root,
# resolved prior annotation artifacts, and built 40 static Stage B diagnostic rows.
PY
python - <<'PY'
# CSV, JSONL, Markdown, protected-path, and no-official-POCR validation checks.
PY
git diff --check
git diff --name-status
git status -sb
```

No live LLM/API command, API key read, DB/checker/timing command, baseline rerun, `compute-local-metrics`, verifier, official metric command, paper rendering, retained-evidence promotion, leaderboard generation, or Track A 120 command was run.
