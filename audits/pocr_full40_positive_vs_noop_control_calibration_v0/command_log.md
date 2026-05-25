# Command Log

Commands were run from `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`. Secret values were not printed; provider checks recorded presence booleans only.

```bash
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,260p' project_control/DECISION_LOG.md
sed -n '1,260p' src/sql_rewrite_bench/pocr/calibration_runner.py
sed -n '1,260p' src/sql_rewrite_bench/pocr/operation_evidence_policy.py
sed -n '1,220p' tests/pocr/test_calibration_runner.py
python -m py_compile src/sql_rewrite_bench/pocr/calibration_runner.py src/sql_rewrite_bench/pocr/operation_evidence_policy.py src/sql_rewrite_bench/pocr/prompt_builder.py
PYTHONPATH=src pytest tests/pocr -q
PYTHONPATH=src python - <<'PY'  # parse all 40 skills and candidate preflight
# safe local parser/candidate checks; no API, DB, checker, timing, or baseline execution
PY
PYTHONPATH=src python - <<'PY'  # provider preflight presence booleans only
# printed only live gate/provider/model/API-key presence booleans, not values
PY
PYTHONPATH=src python -m sql_rewrite_bench.pocr.calibration_runner --live-enabled --case-list common_core_v0 --output-dir audits/pocr_full40_positive_vs_noop_control_calibration_v0
python - <<'PY'  # audit summary/doc generation from CSV/JSONL outputs
PY
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/pocr/calibration_runner.py src/sql_rewrite_bench/pocr/operation_evidence_policy.py src/sql_rewrite_bench/pocr/prompt_builder.py
PYTHONPATH=src pytest tests/pocr -q
PYTHONPATH=src python - <<'PY'  # parse all 40 skills and verify 40 positive + 40 no-op candidates
PY
python - <<'PY'  # CSV/JSONL parse and Markdown non-empty checks
PY
git diff --check
python - <<'PY'  # protected-path review over tracked changes
PY
python - <<'PY'  # added-line and audit-file secret value scans
PY
```

No DB/checker/timing, baseline rerun, `compute-local-metrics`, verifier, user-output integration, route-level POCR aggregation, official metric, paper rendering, or leaderboard command was run.
