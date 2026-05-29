# No Live Boundary

This task used fake-provider fixture tests only.

- No live LLM call occurred.
- No Repair-1 live route was run.
- No Track A 120 row was run.
- No DB execution, checker execution, timing, local metrics, SQLSolver, VeriEQL,
  official metrics, paper rendering, leaderboard output, top-level
  reports/results update, or retained-evidence promotion occurred.

The adapter keeps live provider calls behind:

```text
SQLRB_LLM_ALLOW_LIVE=1
```

and an API key requirement. Missing live gate or missing API key fails closed.

Fake-provider mode uses `SQLRB_LLM_PROVIDER=fake` and does not make network
requests.
