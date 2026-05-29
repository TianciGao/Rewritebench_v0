# Quality Gate Review

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

POCR@planned and POCR@candidate remain D039 promotion views.

POCR@curated remains deferred until a predeclared curated manifest exists.

Micro-average is diagnostic only and not the paper formula.

## Gate Results

- 30 planned rows accounted: yes.
- Candidate-bound rows: 30/30.
- Live calls <= 30: yes, `30` attempted.
- Annotation rows generated: 30.
- Schema-valid / fail-closed rows accounted: yes, `21` schema-valid and `9` fail-closed.
- Replay rows emitted: `30`.
- Route mismatch rows: `0`.
- Candidate mismatch rows: `0`.
- Row metrics CSVs generated: 6.
- Aggregator summary generated: yes.
- No-op possible over-accept cases: `0`.
- POCR@curated remains `NA` / `curated_manifest_missing`: yes.
- Official POCR computed: no.
- Paper-facing metric promoted: no.
- Output committed: no.

## Review

The pilot completed with visible fail-closed annotation rows, primarily malformed provider JSON plus one provider call failure. That is acceptable for a diagnostic pilot because the checkpointed runner, replay, row-metrics exporter, and aggregator preserved those rows instead of silently dropping them. Before a wider Track A 120 expansion, a targeted retry or provider-output robustness review should be considered for the fail-closed rows.
