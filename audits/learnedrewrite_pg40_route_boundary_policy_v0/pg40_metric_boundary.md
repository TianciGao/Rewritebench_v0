# PG40 Metric Boundary

Source packet: `audits/learnedrewrite_pg40_bounded_local_diagnostic_v0/`.

The following values are copied from the PG40 diagnostic packet and its `local_metrics.py` review. They are not recomputed in this policy task.

| Field | Value |
| --- | ---: |
| selected | 40 |
| generated | 29 |
| candidate executable | 23 |
| exact | 17 |
| timed exact rows | 17 |
| mismatch | 6 |
| candidate_execution_failed | 6 |
| fail-closed/no-candidate | 11 |
| Generation Rate | 0.725 |
| Execution Coverage | 0.575 |
| Result Consistency | 0.425 |
| GM speedup | 1.0291029729677286 |
| P10 | 0.8134186116858578 |
| P25 | 0.9784093859740545 |
| P50 | 1.0023559404279565 |
| P75 | 1.014471169398659 |
| P90 | 1.704766251233957 |

This is PostgreSQL-only Common-core 40 local diagnostic evidence. It is not Track A 120, not official metrics, not a paper result, and not retained evidence promotion.

Metric interpretation must remain denominator-aware:

- Generation Rate uses selected PG40 rows as denominator: `candidate_generated / selected`.
- Execution Coverage uses selected PG40 rows as denominator: `candidate_executable / selected`.
- Result Consistency uses selected PG40 rows as denominator: `exact / selected`.
- Speedup summaries apply only over strict exact + timed rows.

SER remains N.A. because no formal verifier evidence was produced. POCR remains deferred/N.A. because no external operation-atom evidence exists.
