# Command Log

All commands were run from `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`.

## Pre-edit Checks

```bash
pwd
git branch --show-current
git status -sb
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,180p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
```

## Read-only Inspection

```bash
sed -n '1,260p' src/sql_rewrite_bench/pocr/prompt_builder.py
sed -n '1,320p' src/sql_rewrite_bench/pocr/live_smoke.py
sed -n '320,700p' src/sql_rewrite_bench/pocr/live_smoke.py
sed -n '1,320p' src/sql_rewrite_bench/pocr/annotation_client.py
sed -n '1,260p' tests/pocr/test_prompt_builder.py
sed -n '1,260p' tests/pocr/test_static_evidence.py
```

## Provider Gate Check

```bash
python - <<'PY'
# Printed only boolean presence/gate status:
# SQLRB_LLM_ALLOW_LIVE=true
# SQLRB_LLM_API_KEY_or_GPTSAPI_API_KEY=true
# SQLRB_LLM_BASE_URL_or_GPTSAPI_BASE_URL_or_default=true
# SQLRB_LLM_MODEL_or_GPTSAPI_MODEL_or_default=true
PY
```

No API key values were printed.

## Implementation

Manual source/test edits were made with `apply_patch`:

- `src/sql_rewrite_bench/pocr/prompt_builder.py`
- `tests/pocr/test_prompt_builder.py`

Focused validation before retry:

```bash
python -m py_compile src/sql_rewrite_bench/pocr/prompt_builder.py
pytest tests/pocr/test_prompt_builder.py tests/pocr/test_static_evidence.py -q
```

## Bounded Live Retry

```bash
python - <<'PY'
# Ran exactly the four authorized fixture cases:
# PERF_0006, CONS_0005, PORT_0003, LONGTAIL_0011.
# Used existing candidate SQL under runs/user/common_core_pg_noop_db_checker/candidate_sql/.
# Wrote safe audit-only outputs under audits/pocr_evidence_ref_alignment_live_retry_v0/.
# Raw prompts and raw provider responses were not stored.
PY
```

## Validation

```bash
find audits/pocr_evidence_ref_alignment_live_retry_v0 -maxdepth 1 -type f -printf '%f\n' | sort
python - <<'PY'
# Parsed audit CSV/JSONL outputs and summarized live/schema/static counts.
PY
python -m py_compile $(rg --files src/sql_rewrite_bench/pocr -g '*.py')
pytest tests/pocr -q
python - <<'PY'
# Parsed 40 Common-core skills.md contracts, confirmed 40/40 PG no-op candidates,
# checked live calls <= 4, CSV/JSONL parseability, Markdown non-empty files,
# official_pocr_computed=false, route_level_pocr_aggregated=false, and protected paths.
PY
rg -n --hidden -S "(sk-[A-Za-z0-9]{12,}|BEGIN (RSA|OPENSSH|DSA|EC|PGP) PRIVATE KEY|api[_-]?key\\s*[:=]\\s*['\"][^'\"]+|password\\s*[:=]\\s*['\"][^'\"]+)" src/sql_rewrite_bench/pocr tests/pocr audits/pocr_evidence_ref_alignment_live_retry_v0 project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md || true
git diff --check
git status -sb
git diff --name-status
```

No DB/checker/timing command, baseline rerun, `compute-local-metrics`, verifier, official POCR computation, route-level POCR aggregation, user-output integration, paper rendering, top-level report/result update, retained-evidence promotion, or leaderboard command was run.
