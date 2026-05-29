# Command Log

Commands were run from `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`. Secrets were not printed.

```bash
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
PYTHONPATH=src python -m py_compile src/cli/main.py src/cli/pocr_diagnostic.py src/sql_rewrite_bench/pocr/user_facade.py src/sql_rewrite_bench/pocr/annotation_resolver.py src/sql_rewrite_bench/pocr/user_output_adapter.py src/sql_rewrite_bench/pocr/diagnostic_output_schema.py
PYTHONPATH=src pytest tests/pocr -q
PYTHONPATH=src pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
rm -rf /tmp/sqlrb_pocr_user_replay_direct_llm_pg40_v0
PYTHONPATH=src python -m cli.main user pocr-diagnostic --enable-pocr-diagnostic --candidate-root runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql --method-id direct_llm_original --route-id direct_llm_original_pg40_user_replay --engine postgres --run-id pocr_user_replay_direct_llm_pg40_v0 --output-root /tmp/sqlrb_pocr_user_replay_direct_llm_pg40_v0/output --annotation-jsonl audits/pocr_real_route_direct_llm_pg40_diagnostic_v0/safe_annotation_outputs.jsonl
python - <<'PY'  # parse temp diagnostic rows and report boundary wording
PY
PYTHONPATH=src python - <<'PY'  # parse all 40 Common-core skills.md files
PY
python - <<'PY'  # CSV parse checks for audit packet
PY
python - <<'PY'  # Markdown non-empty checks for audit packet
PY
git diff --name-only | rg '^(cases/|output/|reports/|results/|runs/|retained_evidence/)|/skills\.md$|/skill/' || true
test -e output && find output -maxdepth 3 -type f | head -20 || echo repo_output_absent
git diff --check
python - <<'PY'  # changed-file secret value scan
PY
```

One inventory validation command was corrected after using a non-existent convenience attribute; the corrected validation counted pools from inventory members and passed.
