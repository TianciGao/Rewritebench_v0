# SQLGlot No-op Over-Accept Review

SQLGlot no-op is a candidate/control route, not a reference.

Across PostgreSQL, MySQL, and Spark row metrics, SQLGlot no-op produced zero Stage-B transformation-supported operation atoms. Possible over-accept cases: 0.

The no-op control therefore remains conservative for this diagnostic expansion. The MySQL and Spark no-op rows have high fail-closed annotation rates because many new provider calls failed, so this is a control pass with boundary rather than a paper-facing claim.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@curated remains deferred until a predeclared curated manifest exists. Micro-average is diagnostic only and not the paper formula.
