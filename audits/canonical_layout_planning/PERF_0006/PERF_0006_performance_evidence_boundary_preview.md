# PERF_0006 Performance Evidence Boundary Preview

Date: 2026-05-16

## Scope

This preview defines how a future `PERF_0006` canonical migration should handle performance-facing artifacts. It is planning-only and does not create, recompute, or validate any performance result.

## Retained Performance Or Timing Artifacts

Static inspection did not find timing, duration, latency, throughput, or speedup artifacts under `cases/PERF/PERF_0006/`.

The retained artifacts are correctness and plan-observability evidence, not timing evidence:

- `runs/result_check.json` records cross-dialect correctness checks over existing outputs.
- TSV outputs record source/positive equality and negative divergence.
- `runs/plan_check.json` records plan-artifact presence.
- PostgreSQL/MySQL JSON plans and Spark text plans record operator/predicate observability.

## Packaging Status

Public-safe correctness and JSON plan artifacts can be copied as retained evidence if hygiene scans pass. Spark plan text artifacts should not be copied raw because they contain local temporary path traces; they should be sanitized or archived through `evidence/runs_retention.yaml`.

## No New Speedup Claim

A future migration must not create a speedup claim. The migration may preserve that the case belongs to the PERF pool and has plan observability evidence, but it must not compute, infer, or report:

- speedup;
- runtime improvement;
- latency improvement;
- throughput;
- performance ranking;
- global leaderboard position.

Correctness-gated performance remains tied to existing paper evidence and denominator policy, not to this migration task.

## Future Handling

If separate timing artifacts are later found outside the case directory, they should be handled by a reports/results retained-evidence map, not by this case migration plan. Any timing publication requires explicit denominator-aware approval.
