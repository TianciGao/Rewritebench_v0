# Transition Notes: `runs/user/` To `output/`

Existing `runs/user/` remains supported as a legacy/development local run surface during transition.

New user-facing runs should target:

- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

Do not delete, move, or rewrite existing `runs/user/` outputs as part of the contract transition.

Do not commit generated `output/` runtime artifacts.

Recommended future ignore policy, to be implemented only when authorized:

```gitignore
output/results/*
output/logs/*
output/reports/*
```

If a placeholder is needed later, use a dedicated `.gitignore` or README policy task; do not create runtime artifacts in this contract task.
