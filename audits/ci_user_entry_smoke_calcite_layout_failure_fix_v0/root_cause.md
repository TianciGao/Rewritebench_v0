# Root Cause

GitHub Actions public logs for runs `#487` / `#488` were not available through the local environment without sign-in, but the failure was reproduced locally in a fresh archive copy.

Reproduction steps:

```bash
rm -rf /tmp/sqlrb_ci_calcite_repro
mkdir -p /tmp/sqlrb_ci_calcite_repro
git archive HEAD | tar -x -C /tmp/sqlrb_ci_calcite_repro
test ! -d /tmp/sqlrb_ci_calcite_repro/runs/user
PYTHONPATH=/tmp/sqlrb_ci_calcite_repro/src PYTHONDONTWRITEBYTECODE=1 \
  pytest /tmp/sqlrb_ci_calcite_repro/tests/user_entry/test_calcite_hep_fail_closed_route.py -q
```

Observed failure:

```text
FileNotFoundError: [Errno 2] No such file or directory:
'/tmp/sqlrb_ci_calcite_repro/runs/user/tmp...'
```

Failing line:

```python
tempfile.TemporaryDirectory(dir=REPO_ROOT / "runs" / "user")
```

Classification:

- Root cause: test fixture assumed `runs/user` already exists.
- Scope: CI/fresh-checkout-only test failure.
- Not caused by the Calcite baseline adapter.
- Not caused by `.github/workflows/user_entry_smoke.yml`.
- Not caused by `scripts/dev/run_user_entry_ci_smoke.py`.
