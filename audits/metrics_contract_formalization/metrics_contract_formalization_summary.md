# Metrics Contract Formalization Summary

Date: 2026-05-17

## Purpose And Scope

This task formalizes Metrics Contract v1 from the maintainer/team-approved paper scope.

It creates `repository_spec/metrics_contract_v1.md`, marks the previous draft as superseded, adds an explainability attribution policy draft, and records the metric suite in audit tables.

No metrics were implemented. No retained-evidence adapter, reproduction CLI, public runner, report renderer, paper table rendering, reports/results migration, DB validation, LLM call, timing workload, denominator update, paper-result update, case-set change, case membership change, case package modification, or raw legacy evidence change was performed.

## Metrics Contract v1 Formalized

Approved primary metric suite:

- Coverage: Generation Rate; Execution Coverage Rate.
- Correctness: Result Consistency Rate; Semantic Equivalence Rate.
- Performance: GM_Speedup; Speedup Ratio Percentiles.
- Explainability: Attribution Coverage.
- Generalization: Cross-Engine Execution; Cross-Engine Consistency; Speedup Retention.

## Key Formalization Choices

- Candidate Failure Rate is removed as a primary metric; failure buckets remain diagnostic.
- Regression@20 is removed as the primary performance-regression metric and may remain only as a legacy diagnostic/comparison.
- Observability / PlanFrontier is replaced in the main metric suite by Explainability / Attribution Coverage.
- PlanFrontier and plan artifacts remain support/diagnostic evidence.
- Support Layer is removed as an independent metric layer; verifier evidence is folded into correctness and Semantic Equivalence Rate support.
- Generation Rate means emitted candidate SQL over planned cases.
- Extraction/readiness remains diagnostic or optional ready-rate support, not the primary Generation Rate.
- Semantic Equivalence Rate is computed only over verifier-decidable result-consistent cases; unknown/undecidable cases are reported separately.
- GM_Speedup and Speedup Ratio Percentiles are computed only over result-consistent timed cases.
- Speedup Retention is `N.A.` unless paired source/target timing exists.
- No global leaderboard is allowed.

## Implementation Boundary

Metrics implementation remains unauthorized. Retained-evidence adapters, paper table rendering, unified reproduction CLI, public runner implementation, and reports/results migration remain unauthorized.

## Unchanged Boundaries

- Reports changed: no.
- Results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.

## Next Safe Action

Review Metrics Contract v1 and the explainability attribution draft. The next safe implementation-adjacent task is a non-mutating retained-evidence adapter design/test plan, still without computing metrics or rendering paper tables.
