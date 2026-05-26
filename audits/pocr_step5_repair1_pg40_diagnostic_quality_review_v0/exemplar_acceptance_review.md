# Exemplar Acceptance Review

Classification: `accepted_with_boundary`.

This run is acceptable as a release v0 diagnostic exemplar with boundary because it is auditable end-to-end, preserves fail-closed invalid/timeout rows, binds annotations to route and candidate SHA, and replay produced 40 diagnostic rows with zero route mismatch and zero candidate mismatch rows. The invalid/timeout rate (5/40) prevents treating it as a polished metric artifact, but the failure mode is visible and bounded.

This is not official POCR. No route-level POCR score is emitted. No paper-facing metric is promoted. This is diagnostic support only.

Schema-invalid and timeout rows remain visible and fail closed. Transformation-supported atom counts are diagnostic counts, not official numerator.

Recommended status: keep as a release v0 diagnostic exemplar with explicit caveats, and prioritize targeted retry / JSON robustness before using the same path for another baseline.
