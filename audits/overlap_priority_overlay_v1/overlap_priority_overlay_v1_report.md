# overlap_priority_overlay_v1 Report

## Purpose And Scope

This audit-only overlay applies the maintainer-approved Option B policy to the 45 candidate-status rows previously blocked by source overlap.

## Option B Policy

- P001 provides generation/readiness evidence.
- P002 provides primary candidate status.
- P003 provides Repair-1 failure enrichment only.
- P003 must not override P002 primary status.

## Rows Resolved

- Overlap rows reviewed: 45.
- Rows resolved by policy: 45.
- Rows still blocked: 0.
- Combined authorized rows in overlay v1: 175.

## Why P003 Cannot Override P002 Primary Status

P003 was approved only as Repair-1 failure enrichment. The overlay therefore records `p003_can_override_primary_status=false` for every row. P002 remains the primary candidate-status source for Repair-1 rows.

## Timing And Metrics Boundary

Timing fields remain unauthorized. No official metrics, paper results, reports/results updates, denominator changes, or paper-result changes are created by this overlay.

## Next Safe Action

Run the overlap normalization refresh and normalized status-only dry-run v3 from the combined overlay. Keep official metrics and timing adapter work separate.
