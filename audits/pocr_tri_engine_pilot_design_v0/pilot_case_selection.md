# Pilot Case Selection

| case_id | pool | reason selected | expected POCR stress | portability / engine risk | decision |
| --- | --- | --- | --- | --- | --- |
| `PERF_0006` | PERF | Previously used in POCR smoke/calibration and has staged filter/projection atoms. | Tests whether filter staging and aggregate rebinding receive transformation-aware evidence rather than presence-only evidence. | TPC-H-style date and aggregation expressions can expose dialect formatting differences. | keep |
| `CONS_0005` | CONS | Previously used in POCR smoke/calibration and has null-sensitive anti-join atoms. | Tests whether annotations capture null-safe `NOT IN` modeling without over-accepting simplified anti-join spans. | Null semantics are dialect-sensitive and useful for prompt stability review. | keep |
| `PORT_0003` | PORT | Represents portability cases and has identifier/order/limit operation atoms. | Tests dialect-normalized identifier and ordering evidence across engines. | PORT cases carry the highest engine-role risk; this case is useful for MySQL/Spark evidence-ref review. | keep |
| `LONGTAIL_0011` | LONGTAIL | Previously used in calibration and has window/rank atoms. | Tests whether dense-rank and max-rank boundary evidence is accepted only when transformation-aware. | Window function representation may vary by engine. | keep |
| `LONGTAIL_0022` | LONGTAIL | Adds derived aggregate/CTE-to-derived stress with comment statistics. | Tests preaggregation and downstream rebinding evidence. | CTE/derived relation formatting and aggregate aliases may vary by engine. | keep |

All five preferred cases remain selected. No fallback substitution is needed because all five have root-level `skills.md`, positive operation atoms, and candidate-bound files for both selected routes across all three engines.
