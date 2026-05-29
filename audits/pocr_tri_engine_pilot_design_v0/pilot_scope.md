# Pilot Scope

The first pilot is intentionally small: 5 cases x 3 engines x 2 routes = 30 planned route-engine rows. This is large enough to exercise route binding, engine-specific candidate files, checkpointed annotation planning, Stage B row-metrics export, and POCR@planned / POCR@candidate aggregation, but small enough to review manually before Track A 120.

The pilot precedes Track A 120 because Track A 120 is 40 cases x 3 engines = 120 planned rows per route. Scaling POCR without first checking tri-engine binding, prompt dialect stability, no-op over-accept behavior, fail-closed rows, and row-metrics export would risk producing hard-to-review diagnostic artifacts.

Direct LLM Repair-1 is selected because its Track A 120 candidate roots are complete across PostgreSQL, MySQL, and Spark and it already has a PostgreSQL PG40 diagnostic exemplar. SQLGlot no-op is selected as a sanity/control route because source-like or low-transform candidates should not be promoted to transformation-supported operation atoms merely from span presence.

SQLGlot optimize is not included in this first tri-engine pilot because prior diagnostics found missing optimize candidates, including PostgreSQL PG40 gaps and incomplete tri-engine roots. No-op candidates must not be substituted for optimize candidates.

PG40 does not substitute for Track A 120. PG40 is PostgreSQL-only; this pilot explicitly includes PostgreSQL, MySQL, and Spark rows to test the tri-engine surface before any broader 120-row route expansion.

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.
