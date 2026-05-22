# Future Fix Prompt

You are working in `Rewritebench_v0`.

Task title: Apply narrow `CONS_0011` order-insensitive checker policy fix

Purpose: Resolve the local Spark diagnostic row-order-only mismatch for `CONS_0011` without changing SQL semantics, global checker behavior, official metrics, timing, reports/results, denominators, paper results, case membership, or raw retained evidence.

Scope:

- Case: `CONS_0011` only.
- Engine focus: local diagnostic Spark no-op path.
- Allowed change: case-local checker policy only, using the repository-supported order-insensitive configuration path.
- Preferred implementation: if the current checker still reads result-row ordering from `checker/normalization.yaml`, add the narrow supported `sort_rows: true` setting for `CONS_0011` only.
- Alternative implementation: if maintainers decide row-order policy belongs in `checker/compare_config.yaml`, implement or use that only in a separately authorized checker-support task and keep the behavior case-scoped.

Do not:

- modify SQL files;
- modify manifests unless separately justified by a case-local policy documentation need;
- modify source code unless explicitly authorized for compare-config support;
- compute official metrics;
- compute timing/speedup;
- update `reports/` or `results/`;
- change denominators, paper results, case membership, or raw retained evidence;
- create a leaderboard;
- create a release tag or export branch.

Required regression checks:

- rerun `CONS_0011` local Spark diagnostic and verify the row-order-only case reaches exact;
- rerun the prior two-case Spark smoke subset (`PERF_0006`, `CONS_0005`);
- rerun representative same-engine PERF, CONS, and LONGTAIL local diagnostic rows;
- include at least one hard-negative/control path or mismatch-control check to confirm row sorting does not mask row-count or value mismatches;
- confirm PORT Spark fail-closed behavior remains unchanged unless separately authorized.

Required audit output:

- create a new audit packet documenting the exact files changed, before/after behavior for `CONS_0011`, regression results, and the local-only boundary;
- update project-control status/log;
- commit and push only intended case-local policy/audit/project-control files.
