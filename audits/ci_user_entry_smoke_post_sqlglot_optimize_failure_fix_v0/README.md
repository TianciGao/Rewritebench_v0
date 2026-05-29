# CI User-Entry Smoke Post SQLGlot Optimize Failure Fix v0

Task: `ci_user_entry_smoke_post_sqlglot_optimize_failure_fix_v0`

Branch: `feature/case-package-v2-external-schema`

This packet records the diagnosis and fix for GitHub Actions `user-entry-smoke` run `#528`, job `B-line user-entry smoke`, shown on the public page at commit `81ec6b3`.

Full GitHub Actions logs were unavailable in this workspace because `gh` is not installed. The failure was reproduced locally with the exact workflow command:

```bash
python scripts/dev/run_user_entry_ci_smoke.py
```

Root cause: `tests/user_entry/test_user_run_outputs.py` still expected `docs/USER_BENCHMARK_GUIDE.md` to document the old internal runner flags `--engine`, `--out`, `python -m sql_rewrite_bench.user_run`, and `scripts/user/run_user_benchmark.py`. The guide now intentionally documents the D035 user-facing facade: `python -m cli.main user evaluate` / `sqlrb user evaluate`, `--engines`, `--output-root`, and `--run-id`.

Fix: update the stale test expectation to validate the current D035 user-facing guide wording. No runtime code, adapter code, docs, cases, schemas, reports, results, or output artifacts were changed.
