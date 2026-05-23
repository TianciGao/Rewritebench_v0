# Schema Fallback Triage

Schema-fallback rows: 4.

- `PORT_0013`
- `LONGTAIL_0022`
- `LONGTAIL_0023`
- `LONGTAIL_0024`

Observed outcomes:

- `PORT_0013` failed at PostgreSQL source execution and also had a schema-fallback generation reason: unsupported column definition `a11 DOUBLE PRECISION`.
- `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024` source SQL executed, but candidates failed after fallback generation caused by unsupported SQL type `timestamp`.

Policy recommendation:

- Future execution/checker passes should exclude `calcite_parse_only_schema_fallback` candidates by default as `not_attempted_manual_review_required`.
- These rows should be re-enabled only after a separately authorized schema-ingestion hardening task.
- They should not be mixed with `calcite_rel_to_sql` candidates in exactness, timing, or route-card interpretation.
