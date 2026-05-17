# normalized_status_only_metrics_dryrun_v3 Report

## Purpose And Scope

This audit-only dry run uses `combined_metric_input_authorization_overlay_v1.csv`, `combined_normalized_candidate_status_overlay_v1.csv`, and the existing R1 `inferred_generated` overlay. It is not official metric computation and does not create paper results.

## Inputs

- Parser-v1 candidate ledger: 600 rows.
- Combined authorization overlay v1: 175 authorized rows.
- Newly authorized overlap rows: 45.
- Still-blocked overlap rows: 0.
- Unresolved rows preserved: 425.
- Inferred generated rows used: 94.

## Difference From v2

v3 adds overlap-priority authorization and normalization before the dry run. The delta table records row-count changes versus v2 by metric, method, pool, and engine.

## Denominator Handling

The planned Track-A same-engine denominator remains unchanged. Unauthorized, still-blocked, and unresolved rows remain visible in denominator/accounting outputs and are not silently dropped.

## Boundaries

- Official metrics computed: no.
- Paper tables rendered: no.
- Timing metrics computed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.

## Next Safe Action

Review the v3 delta and caveats. If accepted, separately authorize official metric-readiness review or SQLGlot status evidence parsing; keep timing and paper rendering separate.
