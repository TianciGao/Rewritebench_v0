# Impacted Artifacts Review

The corrected positive SQL changes the positive-control contract for `LONGTAIL_0011`.

Impact boundary:

- Previous POCR calibration involving `LONGTAIL_0011` should be treated as stale for positive-control calibration if it depended on the old `pos_01.sql`.
- Prior baseline metrics comparing candidates to `source.sql` as oracle are not automatically invalidated by this correction.
- Any positive-control validation evidence for `LONGTAIL_0011` should be refreshed later if needed.
- No paper table was updated in this task.
- No retained evidence was promoted or changed.
- No raw legacy evidence was changed.
- No denominator or case membership changed.

This audit does not claim new official metrics, new POCR values, or replacement paper-facing evidence.
