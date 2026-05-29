# Command Log

Commands run, with secrets redacted by policy:

```text
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,260p' project_control/MIGRATION_STATUS.md
sed -n '1,280p' project_control/DECISION_LOG.md
tail -n 260 project_control/MIGRATION_RUN_LOG.md
sed -n '1,260p' src/sql_rewrite_bench/pocr/annotation_client.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/prompt_builder.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/annotation_schema.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/candidate_resolver.py
python -m py_compile src/sql_rewrite_bench/pocr/checkpointed_annotation_runner.py
pytest tests/pocr/test_checkpointed_annotation_runner.py -q
python - <<'PY' ... print safe live env presence booleans only ... PY
PYTHONPATH=src timeout 180 python -m sql_rewrite_bench.pocr.checkpointed_annotation_runner --live-enabled --case-list PERF_0006,CONS_0005 --max-live-calls 2 --timeout-seconds 60 --max-tokens 4000 --repo-root /home/tianci_gao/code/Rewritebench_v0 --output-root output --run-id pocr_annotation_direct_llm_repair1_pg40_checkpointed_v0 --candidate-root runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql --method-id direct_llm_repair_1 --route-id direct_llm_repair_1_pg40_pocr_diagnostic --engine postgres
python - <<'PY' ... parse checkpointed smoke manifests without printing secrets ... PY
python - <<'PY' ... create audit packet from safe manifests and prior audit ... PY
```

No DB/checker/timing command was run. No baseline adapter was run. No full PG40 annotation command was run.
