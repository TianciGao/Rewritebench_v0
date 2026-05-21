# Runner Consumption Contract

## Resolver

`case_package_resolver.py` should read `manifest.yaml` and expose a validated local diagnostic role object when `local_diagnostic` metadata exists.

Resolver responsibilities:

- validate declared role paths exist;
- expose diagnostic mode;
- expose source-reference engine and query;
- expose target-candidate engine and role;
- expose optional target-reference metadata;
- expose checker comparison intent;
- fail closed on missing or ambiguous required metadata.

The resolver must not invoke adapters, execute DB queries, run checkers, compute metrics, or infer roles from SQL text.

## User Runner / Execution Planner

`user_run.py` or a future execution planner should choose:

- same-engine local diagnostic path when no cross-dialect metadata exists;
- explicit cross-dialect path when `diagnostic_mode: cross_dialect_reference` exists;
- fail-closed row status when metadata is incomplete, manual-review-only, unsupported, or backend-missing.

The runner must not silently replace `sql/source.sql` with `sql/pos_01.sql`.

## Engine Router

`engine_execution.py` should execute declared source-side and target-side queries through their explicit engines.

Expected behavior:

- source-reference execution uses `source_reference.engine`;
- target-candidate execution uses `target_candidate.engine`;
- unsupported engines fail closed;
- MySQL-like source-reference cases require future MySQL backend support;
- Spark remains fail-closed until explicitly implemented.

No silent fallback to PostgreSQL is allowed.

## Local Checker

`local_result_checker.py` should consume declared result artifact paths:

- source-reference result JSONL;
- target-candidate result JSONL;
- checker config paths;
- normalization config;
- compare config.

The checker must not execute SQL, perform candidate preflight, compute speedup, or become a formal SQL verifier.

## Ledger

`user_ledger.py` should record:

- metadata missing or ambiguous status;
- backend missing or not configured status;
- source-reference execution status;
- target-candidate execution status;
- checker attempted status;
- local exact/mismatch status;
- local failure bucket priority.

`candidate_preflight_failed` remains earlier than engine execution. Source-reference or target-candidate execution failures come from engine execution. Checker failures and mismatches come after checker handoff.

## Strict Non-Inference Rules

- Do not infer roles from file names alone.
- Do not infer roles from SQL text.
- Do not infer execution roles from pool name alone.
- Do not automatically use `pos_01.sql` as source oracle.
- Do not scan `cases/` for Common-core membership.
- Do not update `case_sets/`, reports, results, retained evidence, denominators, or paper results.

## Non-Goals

- MySQL/Spark implementation in P1.
- Official metrics.
- Timing/speedup.
- Paper table rendering.
- Reports/results migration.
- Global leaderboard.
