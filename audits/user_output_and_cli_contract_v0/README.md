# User Output And CLI Contract v0

Verdict: `completed`

This audit/design packet defines the user-facing output contract and CLI/interface contract for SQL-RewriteBench local evaluation workbench v0, aligned with D034 and D035.

This task did not implement output writing, CLI code, verifier integration, timing collection, metrics computation, physical layout migration, reports/results updates, retained-evidence promotion, paper rendering, or leaderboard output.

## Contract Summary

Future user-facing local runs should write to the D035 shape:

```text
output/
  results/<run_id>/
  logs/<run_id>/
  reports/<run_id>/
```

The older `output/<run_id>/...` shape is historical context only.

The preferred public command shape is:

```bash
sqlrb user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --output-root output \
  --run-id <run_id> \
  [--collect-timing] \
  [--verifier verieql] \
  [--verifier sqlsolver]
```

`src/cli` is the target public facade location. `src/sql_rewrite_bench` remains the internal implementation package.

## Draft Spec

This task also creates `repository_spec/user_output_contract_v0_draft.md` as a draft design/spec reference. It is not an implementation and does not create output runtime directories.

## Next Safe Action

Authorize an implementation planning task for the user-facing output writer and CLI facade, still without physical repository layout migration.
