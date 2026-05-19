# Postgres PERF Batch Smoke Command Log

This log records concise command outcomes only. It does not include secrets, DB passwords, full DSNs, `PGPASSWORD`, raw long stdout/stderr dumps, or environment values.

## Preflight

- `pwd && git branch --show-current && git remote -v && git status -sb && git log --oneline -5 && git rev-list --left-right --count HEAD...origin/main`: passed; release repo on `main`, aligned with `origin/main`, clean before intended task writes.
- Read project-control files, DB/checker batch plan packet, runner implementation boundaries, SQLGlot adapter, run-artifact policy, and Common-core metadata: passed.
- `psql --version`: passed; psql CLI available.
- `psql -c "select 1;"`: passed; connectivity verified without logging credentials or environment values.
- `python -c "import sqlglot"`: passed; SQLGlot version observed as `30.2.1`.
- Existing output directory check for `runs/user/postgres_perf_sqlglot_noop_batch_smoke`: absent before batch run.
- Static selected-case asset check: passed for `PERF_0007`, `PERF_0008`, `PERF_0013`, and `PERF_0017`.

## Batch Execution

Created:

`audits/b_line_postgres_perf_batch_smoke_v0/postgres_perf_batch_cases.txt`

with exactly:

```text
PERF_0007
PERF_0008
PERF_0013
PERF_0017
```

Ran:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list audits/b_line_postgres_perf_batch_smoke_v0/postgres_perf_batch_cases.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/postgres_perf_sqlglot_noop_batch_smoke \
  --enable-db-execution \
  --enable-checker
```

Outcome:

- selected rows: 4
- candidate-generated rows: 4
- source execution success rows: 4
- candidate execution success rows: 4
- checker success rows: 4
- checker mismatch rows: 0
- local exact rows: 4
- local mismatch rows: 0

## Output Verification

- Verified `ledger.csv`, `summary.json`, `report.md`, `failures.csv`, and `selected_cases.csv` exist.
- Verified candidate SQL, source result, candidate result, and checker result artifacts exist for all four rows.
- Verified each ledger row has `local_execution_only=true`, `official_metric_input=false`, and `retained_evidence_input=false`.
- Verified statuses use approved vocabulary and failure bucket is `none` for each row.
- Verified no timing or speedup columns were introduced in the audit results CSV.
- Verified no leaderboard output exists.

## Boundary Checks

- `git status --short cases case_sets inventory reports results`: passed; no protected path output.
- `git status --short runs/user`: passed; no staged/tracked user-run output.
- No legacy repo inspection or modification was performed.
- No official metrics, timing, paper tables, reproduction CLI, retained-evidence adapter, reports/results update, denominator change, paper-result change, or leaderboard output was created.

## Validation

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`: passed.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/dev/smoke_ledger_fixtures.py`: passed.
- Summary JSON invariant check: passed.
- CSV checks: passed.
- `git diff --check`: passed.
