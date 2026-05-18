# Release Smoke Command Log

This log records short command summaries only. It omits raw stdout/stderr dumps and environment details that are not needed for audit traceability.

## Release Repo Preflight

```bash
pwd
git branch --show-current
git remote -v
git status -sb
git log --oneline -5
```

Outcome: passed. Release repo was on `main`, tracking `origin/main`, and clean before audit writes.

## Temporary Clone

```bash
rm -rf /tmp/sqlrb_user_entry_release_smoke
mkdir -p /tmp/sqlrb_user_entry_release_smoke
git clone /home/tianci_gao/code/Rewritebench_v0 /tmp/sqlrb_user_entry_release_smoke/Rewritebench_v0_smoke
```

Outcome: passed.

## Venv And Editable Install

```bash
python -m venv .venv-smoke
.venv-smoke/bin/python -m pip install -e .
```

Outcome: passed. The package installed as `sql-rewrite-bench` in editable mode.

## Help Checks

```bash
.venv-smoke/bin/python -m sql_rewrite_bench.user_run --help
.venv-smoke/bin/python scripts/user/run_user_benchmark.py --help
```

Outcome: passed. Both commands returned successfully and exposed the user-entry CLI options.

## Case-list Setup

```bash
printf 'PERF_0006\nPERF_0007\n' > tmp_smoke_cases.txt
```

Outcome: passed.

## Dry-run Smoke

```bash
.venv-smoke/bin/python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list tmp_smoke_cases.txt \
  --adapter-command ".venv-smoke/bin/python tests/user_entry/fixtures/dummy_adapter.py" \
  --out runs/user/release_smoke_dry_run \
  --dry-run
```

Outcome: passed. Selected rows: 2. Adapter invocations: 0. Candidate rows: 0.

## Dummy Adapter Smoke

```bash
.venv-smoke/bin/python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --pool PERF \
  --engine postgres \
  --case-list tmp_smoke_cases.txt \
  --adapter-command ".venv-smoke/bin/python tests/user_entry/fixtures/dummy_adapter.py" \
  --out runs/user/release_smoke_adapter
```

Outcome: passed. Selected rows: 2. Adapter invocations: 2. Candidate rows: 2.

## Output And Boundary Checks

```bash
git status --short runs/user
git status --short --ignored runs/user
git status --short cases case_sets inventory reports results
```

Outcome: passed. `runs/user/` smoke outputs were ignored and unstaged. Protected paths had no status output.

## Release Repo Validation

```bash
python scripts/dev/smoke_ledger_fixtures.py
git diff --check
git status -sb
```

Outcome: fixture smoke passed. Final diff/status checks were rerun after audit writeback.
