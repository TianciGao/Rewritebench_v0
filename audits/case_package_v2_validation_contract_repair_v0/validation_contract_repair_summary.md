# Validation Contract Repair Summary

## Purpose and scope

This task adopted the v2 three-file validation contract for the 32 already converted cases only. It did not convert Wave C cases and did not run DB/checker execution.

Target validation surface:

```text
validation/run_validation.sh
validation/run_plan_collection.sh
validation/run_engine_queries.py
```

## Design decision

The third file is retained as a thin case-local shared-runner entrypoint, not as copied per-case implementation. Engine execution and plan collection logic now has stable shared fail-closed entrypoints under `src/sql_rewrite_bench/validation/`.

## Shared runner module summary

- `src/sql_rewrite_bench/validation/engine_query_runner.py` parses `--case`, `--mode`, `--engine`, `--target`, and `--out`, validates manifest/schema/SQL path shape, rejects case-local `runs/` output, and fails closed without DB execution.
- `src/sql_rewrite_bench/validation/plan_collection_runner.py` delegates to the shared engine runner in plan-collection mode.
- No shared module opens database connections, executes SQL, collects plans, computes metrics, writes reports/results, or creates leaderboard output.

## Cases updated

- Target cases updated: 32/32.
- `validation/run_engine_queries.py` shims added: 32.
- Manifest validation sections updated: 32.
- Existing shell wrappers replaced with uniform thin wrappers that delegate to the local shim and pass through caller arguments.

## Validator and tests

- Static v2 resolver now requires `validation.run_engine_queries` and checks that the case-local Python file is a short shim importing `sql_rewrite_bench.validation.engine_query_runner`.
- Tests updated for missing manifest field, missing shim file, copied implementation markers, and static no-execution behavior.
- Unit tests passed: 19/19.
- Static validators passed: 32/32 target cases.

## Protected boundary summary

- Wave C cases modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.
- Case-local runs restored: no.
- `evidence/cases/` restored: no.
- Old validation scripts restored: no.

## Exact next safe action

Run a read-only post-repair validation contract review for the 32 converted cases, or authorize the first Wave C writable conversion subwave using the repaired three-file validation contract, starting with `PORT_0005` only.
