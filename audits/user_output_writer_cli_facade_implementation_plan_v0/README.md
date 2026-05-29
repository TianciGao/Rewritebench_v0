# user_output_writer_cli_facade_implementation_plan_v0

Verdict: completed.

This packet plans the Step 2 implementation of the user-facing output writer and `src/cli` facade after D034, D035, and `user_output_and_cli_contract_v0`. It is implementation planning only.

The plan keeps the current `runs/user/<run_id>/` surface as the transition source of truth and introduces a future user-facing export surface under:

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

The proposed output writer module is `src/sql_rewrite_bench/user_output.py`. The proposed public facade target is `src/cli`, with `src/sql_rewrite_bench` remaining the internal implementation package.

No output writer, CLI, verifier, physical layout migration, Common-core run, timing collection, metrics computation, official reports/results update, retained-evidence promotion, paper rendering, or leaderboard output was implemented.

Recommended next safe action: authorize Phase 2A only, adding the output writer skeleton and bounded-smoke export path while preserving `runs/user/` compatibility and avoiding top-level `reports/` and `results/`.
