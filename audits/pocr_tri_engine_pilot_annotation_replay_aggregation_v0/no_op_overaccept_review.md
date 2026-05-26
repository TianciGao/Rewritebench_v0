# SQLGlot No-Op Over-Accept Review

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

SQLGlot no-op is used here as a sanity/control route. Across PostgreSQL, MySQL, and Spark, the aggregator summary reports `0` Stage-B transformation-supported operation atoms for the no-op route.

Result: no-op control passed for this pilot. No no-op route-engine row produced transformation-supported operation atoms, so no possible over-accept cases were identified from the row metrics.

Presence-only and insufficient-transformation-evidence atoms remain diagnostic quality signals only. Micro-average is diagnostic only and not the paper formula. POCR@curated remains deferred until a predeclared curated manifest exists.
