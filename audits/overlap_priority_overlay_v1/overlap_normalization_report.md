# overlap_normalization_v1 Report

## Purpose And Scope

This audit-only refresh preserves the existing 130 normalized candidate-status rows and normalizes only newly authorized overlap rows from `combined_metric_input_authorization_overlay_v1.csv`.

## Summary

- Previous normalized rows: 130.
- Newly normalized overlap rows: 45.
- Combined normalized rows: 175.
- Still-blocked overlap rows: 0.
- Unresolved rows excluded: 425.
- Rows needing manual mapping: 27.

## Boundary

The script reads the existing mapping table and applies the same conservative mapping semantics. It does not modify `normalized_candidate_status_overlay_v0.csv`, does not fill timing fields, does not compute metrics, and does not create paper results.

## Next Safe Action

Use the combined normalized overlay in the audit-only normalized status-only dry-run v3. Treat manual-mapping rows as caveats, not official metric inputs.
