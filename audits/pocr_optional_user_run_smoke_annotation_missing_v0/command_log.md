# Command Log

Initial checks:

```text
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,180p' project_control/MIGRATION_STATUS.md
sed -n '1,260p' project_control/DECISION_LOG.md
```

Pre-smoke validation:

```text
test -d runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql
find runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql -maxdepth 1 -name '*__postgres.sql' | wc -l
PYTHONPATH=src python -m py_compile src/cli/main.py src/cli/pocr_diagnostic.py src/sql_rewrite_bench/pocr/user_facade.py src/sql_rewrite_bench/pocr/user_output_adapter.py src/sql_rewrite_bench/pocr/diagnostic_output_schema.py
PYTHONPATH=src pytest tests/pocr -q
PYTHONPATH=src pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
```

Smoke command:

```text
rm -rf /tmp/sqlrb_pocr_user_smoke_annotation_missing_v0
PYTHONPATH=src python -m cli.main user pocr-diagnostic \
  --enable-pocr-diagnostic \
  --candidate-root runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql \
  --method-id direct_llm_original \
  --route-id direct_llm_original_pg40_user_smoke \
  --engine postgres \
  --run-id pocr_user_smoke_annotation_missing_v0 \
  --output-root /tmp/sqlrb_pocr_user_smoke_annotation_missing_v0/output
```

Post-smoke checks:

```text
PYTHONPATH=src python - <<'PY'
# Parsed diagnostic rows and summary, checked row count, annotation_missing status,
# required false/true diagnostic flags, and required report boundary wording.
PY
PYTHONPATH=src python -m cli.main user pocr-diagnostic
find /tmp/sqlrb_pocr_user_smoke_annotation_missing_v0/output -type f | sort
python - <<'PY'
# Parsed audit CSVs.
PY
python - <<'PY'
# Checked audit Markdown files are non-empty.
PY
PYTHONPATH=src python - <<'PY'
# Parsed all 40 Common-core root-level skills.md contracts.
PY
git diff --name-only | rg '^(cases/|output/|reports/|results/|runs/|retained_evidence/)|/skills\.md$|/skill/' || true
rg -n "sk-[A-Za-z0-9_\-]{20,}|Authorization:\s*Bearer\s+[A-Za-z0-9_\-.]+|(OPENAI_API_KEY|SQLRB_LLM_API_KEY)\s*=\s*[A-Za-z0-9_\-]{12,}" audits/pocr_optional_user_run_smoke_annotation_missing_v0 project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md || true
test ! -e output
git diff --check
git diff --cached --name-status
git diff --cached --name-only | rg '^(cases/|output/|reports/|results/|runs/|retained_evidence/)|/skills\.md$|/skill/' || true
git diff --cached --name-only -z | xargs -0 rg -n "sk-[A-Za-z0-9_\-]{20,}|Authorization:\s*Bearer\s+[A-Za-z0-9_\-.]+|(OPENAI_API_KEY|SQLRB_LLM_API_KEY)\s*=\s*[A-Za-z0-9_\-]{12,}" || true
```

No live API, API-key read, DB/checker/timing, baseline, local metrics, verifier, official POCR, route-level POCR aggregation, paper rendering, retained-evidence promotion, or leaderboard command was run.
