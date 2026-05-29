# Table 4. Metric Availability And Boundary

| paper_metric_name | layer | current_status | computed_or_NA_reason | boundary |
|---|---|---|---|---|
| Generation Rate | Coverage | computed for approved local diagnostic scopes with local_metrics.py outputs | Computed for Track A 120 canonical local diagnostics and PostgreSQL-only PG40 bounded prior-method diagnostics; N.A. for verifier support rows | Local diagnostic only; not official metrics or leaderboard. |
| Execution Coverage Rate | Coverage | computed for approved local diagnostic scopes with local_metrics.py outputs | Computed where generated candidate execution status exists under the approved scope; N.A. for verifier support rows | Unsupported and missing-candidate rows remain denominator-visible where applicable. |
| Result Consistency Rate | Correctness | computed for approved local diagnostic scopes with local_metrics.py outputs | Computed as exact/result-consistent count over selected/planned denominator for the approved scope | Local checker exactness is not formal verifier evidence. |
| Semantic Equivalence Rate | Correctness | N.A. or coverage_limited | No official formal verifier evidence covers the approved route scopes; SQLSolver and VeriEQL remain coverage-limited support | No official Semantic Equivalence Rate is produced; verifier support is not a rewrite-generation baseline. |
| GM Speedup Ratio | Performance | computed for approved local diagnostic scopes with local_metrics.py outputs | Computed only over strict exact/result-consistent timed rows | Not global route quality; missing timing is not zero. |
| Speedup Ratio Percentiles | Performance | computed for approved local diagnostic scopes with local_metrics.py outputs | P10/P25/P50/P75/P90 copied from existing local_metrics.py review outputs over strict exact timed rows | Do not compare Track A 120 and PG40 as a global ranking. |
| Positive Operation Coverage Rate | Interpretability | deferred / N.A. | External operation-atom evidence and script are required; tag_slices are diagnostic support only | No Positive Operation Coverage Rate is computed in this packet. |
| Cross-Engine Execution Coverage Rate | Generalization | N.A. | No separate approved cross-engine denominator/evidence packet is available for these paper-facing drafts | Do not infer cross-engine coverage from same-engine Track A rows. |
| Cross-Engine Result Consistency Rate | Generalization | N.A. | No separate approved cross-engine denominator/evidence packet is available for these paper-facing drafts | Do not infer cross-engine result consistency from same-engine Track A rows. |
| Cross-Engine GM Speedup Ratio | Generalization | N.A. | Target-engine paired timing evidence is absent | Do not compute or imply cross-engine speedup. |
