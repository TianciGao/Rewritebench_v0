# Bounded Diagnostic Report

## Selected-Row Rationale

The run selected the full Common-core PostgreSQL slice: 40 planned rows. No MySQL or Spark row was selected, and this was not a Track A 120 run.

## Provider Status

Provider preflight confirmed the live gate and provider configuration by presence only: `SQLRB_LLM_ALLOW_LIVE=1`, provider `openai_compatible`, configured base URL host, model `gpt-5.4`, and API key present without printing the value. Raw response saving was disabled.

## Generation / Extraction / Preflight

- selected rows: 40
- live calls attempted: 40
- candidates generated: 40
- extraction failures: 0
- candidate preflight passed: 40
- fail-closed rows: 0

## DB / Checker / Timing

- source executable: 40
- candidate executable: 38
- exact: 37
- mismatch: 1
- candidate execution failed: 2
- timed rows from timing ledger: 33

Status counts:
- execution status: {'candidate_execution_success': 38, 'candidate_execution_failed': 2}
- checker status: {'checker_success': 37, 'checker_not_enabled': 2, 'checker_mismatch': 1}
- exact status: {'exact': 37, 'not_exact_due_to_execution_failure': 2, 'mismatch': 1}
- timed status: {'timed': 33, 'not_eligible': 7}

## Local Metrics

The requested `compute-local-metrics` command failed before writing local metric outputs because the aggregate run id matched the existing evaluate run directory and the CLI stale-output guard rejected non-aggregate artifacts. No metric rates were hand-computed.

## Failure Frontier

Dominant failure buckets:
- none: 37
- candidate_execution_failed: 2
- mismatch: 1

Failure rows:
- `PERF_0013`: candidate execution failed; safe excerpt: `psql:/home/tianci_gao/code/Rewritebench_v0/runs/user/rbot_gpt54_pg40_bounded_diagnostic_v0/workspaces/PERF_0013/postgres/execution/candidate_query.sql:30: 错误:  字段 s.suppkey 不存在 / LINE 26:  AND l.l_suppkey = s.suppkey /                             ^`
- `LONGTAIL_0011`: candidate execution failed; safe excerpt: `psql:/home/tianci_gao/code/Rewritebench_v0/runs/user/rbot_gpt54_pg40_bounded_diagnostic_v0/workspaces/LONGTAIL_0011/postgres/execution/candidate_query.sql:26: 错误:  不允许嵌套调用窗口函数 / LINE 10:         MAX(DENSE_RANK() OVER (PARTITION BY p.OwnerUserId OR... /                      ^`
- `PORT_0013`: checker mismatch in PostgreSQL target run with cross-dialect source-reference handling.

## LONGTAIL_0011

`LONGTAIL_0011` still fails candidate execution. The candidate contains a nested window-function shape, and PostgreSQL rejects it with `不允许嵌套调用窗口函数` / nested window-function calls are not allowed. This matches the key failure mode observed in the six-row smoke.

## Source-Like / No-Op Behavior

The facade reported `source_like_status=changed` for all 40 generated candidates. Diagnostic source-like/no-op count is therefore 0. This is not POCR and is not a ranking metric.

## Readiness

The adapted R-Bot route is ready for a PostgreSQL route boundary/policy packet because the PG40 diagnostic completed, but metric promotion is blocked by the local-metrics aggregate-output guard until the command shape or aggregate output policy is addressed. It is not ready for Track A 120 without a separate policy.

## Boundaries

This is adapted GPT-5.4 local diagnostic evidence only. It is not original R-Bot reproduction, not Track A 120, not official metrics, not verifier evidence, not paper evidence, not retained evidence, and not leaderboard input.
