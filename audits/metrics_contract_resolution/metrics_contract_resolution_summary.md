# Metrics Contract Resolution Summary

Date: 2026-05-17

## Purpose And Scope

This audit resolves the draft metric contract against the maintainer-provided updated paper metric scope.

This task does not implement metrics, implement retained-evidence adapters, implement a unified reproduction CLI, implement a public runner, render paper tables, copy reports/results, run DB engines, compute metrics, change denominator values, change paper results, change case membership, modify case packages, or modify raw legacy evidence.

No project-root manuscript or paper-scope file was discoverable in the release repository, so the maintainer-provided scope in the task prompt is treated as authoritative for this alignment.

## What Changed From The Previous Decision Packet

The prior decision packet listed multiple open alternatives. This resolution narrows the draft contract to the updated paper metric suite:

- Coverage: `Generation Rate`, `Execution Coverage Rate`.
- Correctness: `Result Consistency Rate`, `Semantic Equivalence Rate`.
- Performance: `GM_Speedup`, `Speedup Ratio Percentiles`.
- Explainability: `Attribution Coverage`.
- Generalization: `Cross-Engine Execution`, `Cross-Engine Consistency`, `Speedup Retention`.

Key changes:

- `Generation Rate` now means candidate SQL generation only.
- Extraction/readiness variants are not second primary Generation Rate variants.
- `Candidate Failure Rate` is removed as a primary metric.
- Failure buckets remain diagnostic.
- `Regression@20` is replaced or demoted by `Speedup Ratio Percentiles`.
- `Attribution Coverage` becomes the explainability metric direction, with implementation deferred.
- The independent Support Layer is removed; verifier evidence is folded into correctness and semantic-equivalence discussion.
- `Speedup Retention` is part of generalization, but is `N.A.` unless paired target-engine timing exists.

## Removed Or Demoted Metrics

- `Candidate Failure Rate`: removed as primary; failure buckets diagnostic only.
- `Regression@20`: not primary; optional diagnostic or legacy comparator only.
- `PlanFrontier` / broad observability: folded into explainability via `Attribution Coverage` and retained evidence inputs.
- `SupportRate` / Support Layer: removed as independent layer; verifier evidence supports correctness.
- Parseability, extractability, runnable SQL, readiness, unsupported, and preflight-blocked statuses remain diagnostic fields unless separately finalized later.

## Deferred Metrics

- `Attribution Coverage`: direction accepted, implementation deferred until attribution schema and denominator are specified.
- `Semantic Equivalence Rate`: depends on verifier decidability and available semantic-equivalence evidence.
- `Speedup Retention`: `N.A.` unless paired target-engine timing is available.

## Implementation Blockers

- Retained-evidence adapters are not implemented.
- Ledger rows have not been materialized.
- Attribution schema is not finalized.
- Paired timing for speedup retention is not guaranteed.
- Paper table rendering is not authorized.
- Public runner and unified reproduction CLI are not authorized.

## Denominator Boundaries

- Common-core 40 remains unchanged.
- Track A same-engine planned rows remain 120.
- Same-engine rewrite metrics use Track A denominator semantics.
- Control rows remain separate from candidate rows.
- PORT/generalization rows remain separate from same-engine Track A rows.
- Verifier evidence is support evidence inside correctness discussion, not a rewrite-generation baseline.
- No global leaderboard is allowed.

## Next Safe Action

Review the aligned draft contract and approve or revise the remaining implementation prerequisites before creating retained-evidence adapters, metric computation, paper table rendering, a unified reproduction CLI, or public runner outputs.
