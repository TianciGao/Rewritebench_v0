# No-Op Over-Accept Review

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

The SQLGlot no-op sanity/control route still has zero Stage-B transformation-supported operation atoms after targeted retry across PostgreSQL, MySQL, and Spark. Possible over-accept cases: 0.

The MySQL no-op retry converted `LONGTAIL_0022` from provider-call-failed to schema-valid, but Stage B did not count any transformation-supported operation atom. This supports the control expectation that source-like or low-transform candidates are not accepted merely because candidate SQL contains source-like spans.

Manual review for no-op over-accept is not required by this pilot result. The route remains diagnostic/control evidence only. Micro-average is diagnostic only and not the paper formula.
