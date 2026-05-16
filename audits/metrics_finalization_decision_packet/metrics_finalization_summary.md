# Metrics Finalization Decision Packet

Date: 2026-05-17

## Purpose And Scope

This decision packet organizes the remaining SQL-RewriteBench metric-contract choices for maintainer/team review before implementation.

This task does not implement metrics. It does not implement retained-evidence adapters, a unified reproduction CLI, a public runner, or a paper table renderer. It does not copy reports/results, run DB engines, regenerate evidence, compute timing, update paper tables, change denominator values, change case membership, or modify raw legacy evidence.

## Current Stable Paper Contract

The current paper direction remains stable:

- Common-core v0 is the public v0 benchmark line.
- Common-core 40 remains fixed.
- Track A same-engine planned denominator remains 120 rows.
- Reporting must remain role-aware and denominator-aware.
- No global leaderboard is allowed.
- Correctness gate comes before performance interpretation.
- Performance interpretation is limited to exact and timed eligible rows.
- Hard negatives are checker controls.
- Verifier support is support evidence and not a rewrite-generation baseline.
- PORT portability evidence has bounded cross-engine semantics and must not be collapsed into Track A same-engine rows.

## Proposed Decision Areas

The packet asks the maintainer/team to decide:

- which current metric families keep their names and definitions;
- which metrics need clarified names or numerator/denominator wording;
- which outputs become support or diagnostic evidence rather than primary metrics;
- whether Regression@20 remains or is supplemented/replaced by quartile/distribution reporting;
- whether parseability, SQL extractability, and runnable SQL become first-class fields or metrics;
- how PlanAvailability and PlanFrontier should be separated;
- how failure buckets should be named and reported;
- what user submission and output-root format should be used later.

## High-level Recommendation

Keep the stable denominator and role-aware reporting contract unchanged. Treat `Exact@planned`, `ExecutionCoverage`, negative-rejection reporting, and exact/timed performance reporting as stable families, but require final wording before implementation.

Recommended direction for open choices:

- Keep Regression@20 for paper continuity only if its denominator and threshold remain defensible.
- Add quartile/distribution performance summaries as the safer public workbench view.
- Make parseability/extractability/runnable SQL diagnostic fields first, not primary headline metrics.
- Treat observability as its own metric family and evidence layer, not as performance or correctness.
- Keep verifier support support-only.
- Keep hard-negative rows in the control scaffold, not rewrite-candidate denominators.

## Blocking Decisions

Implementation remains blocked on:

- final performance regression choice;
- final exact/executed/timed gate wording;
- parseability/extractability/runnable SQL definitions;
- observability wording and PlanAvailability versus PlanFrontier split;
- failure bucket taxonomy;
- user submission `candidate_id` and output format;
- retained LLM evidence scope: frozen-only versus rerunnable.

## Ledger And Row-grain Connection

The decision packet uses the typed ledger row-grain policy:

- `rewrite_candidate_cell` feeds same-engine candidate metrics when denominator eligible.
- `control_cell` feeds source-positive and hard-negative checker evidence.
- `plan_observability_artifact` feeds observability only.
- `portability_candidate_cell` feeds PORT portability metrics only.
- `verifier_support_pair` is support-only.
- `retained_summary_artifact` is traceability and comparison material.
- `user_run_candidate_cell` is future public-run output and remains unimplemented.

## Unchanged Boundaries

- Common-core 40 unchanged.
- Track A 120 planned rows unchanged.
- Role-aware and denominator-aware reporting unchanged.
- No global leaderboard.
- Correctness gate before performance.
- Verifier support is not a rewrite-generation baseline.
- Hard negatives are checker controls.
