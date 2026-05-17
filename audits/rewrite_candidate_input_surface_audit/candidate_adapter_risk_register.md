# Candidate Adapter Risk Register

## Scope

This register records risks for future adapters that may fill `rewrite_candidate_cell` fields after the Track-A scaffold. It is planning only and does not authorize implementation, retained-evidence parsing, timing parsing, metrics computation, or paper rendering.

## Risks And Mitigations

| Risk | Why It Matters | Mitigation |
|---|---|---|
| Parsing legacy reports/results/runs directly | Legacy artifacts may contain local paths, logs, mixed workspaces, prompt/model traces, and ambiguous row grain. | Require separate production retained-evidence adapter authorization, input manifests, public-hygiene checks, and fail-closed validation. |
| Using summary tables as metric facts | Paper/result summaries may be aggregated, denominator-specific, or route-mixed; converting them into row facts can silently change metrics. | Treat summaries as `retained_summary_artifact` or adapter planning inputs until lower-grain rows are parsed and validated. |
| Timing fields | `latency_ms`, `speedup_ratio`, `timed`, and `timing_eligible` are performance-critical and missing timing must not become zero. | Require separate timing adapter, timing eligibility policy, and validation before any performance metric. |
| Repair mixed-source timing | `direct_llm_repair_1` can mix original candidate generation, repair attempts, repaired SQL, execution evidence, and timing references. | Split generation, repair, execution, and timing provenance before any status or timing fill. |
| SQLGlot no-op source-like rows | No-op output may be textually close to source SQL and could be confused with source controls. | Preserve `rewrite_candidate_cell` method identity and do not inherit control-cell execution/exactness. |
| Calcite fail-closed semantics | Fail-closed behavior can mean unsupported, blocked, no candidate, failed generation, or generated-but-failed depending on artifact context. | Define fail-closed status taxonomy before filling `generated`, `ready`, `result_status`, `failure_stage`, or `failure_type`. |
| Using `retained_evidence_candidate_map.csv` as production input | The map is a release-repo audit inventory with legacy references, not row-grain production evidence. | Use it only as metadata/manifest planning unless a later task explicitly authorizes a parser and validates row grain. |
| Plan artifacts as explainability facts | Plan files support observability but do not by themselves establish Attribution Coverage. | Route through a future `plan_observability_adapter` and attribution policy implementation. |
| Premature `metric_input_authorized=true` | Marking rows metric-eligible before retained-evidence validation can enable incorrect metric computation. | Keep `metric_input_authorized=false` until production ledger validation and metric implementation are explicitly authorized. |
| Route mixing | Direct LLM, repair, SQLGlot optimize, SQLGlot no-op, and Calcite HEP have distinct route semantics. | Keep method/route boundaries explicit and reject global-leaderboard or route-collapsed outputs. |

## Blockers Before Metric Use

- Candidate status fields are not filled.
- Production retained evidence has not been parsed.
- Timing evidence has not been adapted.
- Plan artifacts have not been adapted.
- Metric implementation remains unauthorized.
- Paper table rendering remains unauthorized.

## Mitigation Plan

1. Keep the current scaffold as planned row grain only.
2. If authorized, implement a bounded `candidate_status_adapter_v0` for non-timing fields only and fail closed when release summaries do not prove row grain.
3. Implement timing and plan adapters only as separate later tasks.
4. Validate any adapter output with the production ledger validator skeleton before any metric computation.
5. Keep `metric_input_authorized=false` until a later explicit authorization changes it.
