# CLI Placeholder Behavior

Current behavior should remain fail-closed:

```bash
sqlrb user evaluate --verifier verieql ...
sqlrb user evaluate --verifier sqlsolver ...
```

These flags must not pretend verifier integration exists. They should fail before invoking the evaluation pipeline until implementation is separately authorized.

Future commands may include:

```bash
sqlrb user verify --run-id <run_id> --tool verieql
sqlrb user verify --run-id <run_id> --tool sqlsolver
```

Future command constraints:

- Read existing local user-run output.
- Write only under `output/results/<run_id>/verifier/`, `output/logs/<run_id>/verifier.log`, and `output/reports/<run_id>/verifier_summary.md`.
- Do not update top-level `reports/` or `results/`.
- Do not compute official metrics.
- Do not produce leaderboard/ranking/winner output.
- Keep VeriEQL and SQLSolver as support tools, not rewrite baselines.
