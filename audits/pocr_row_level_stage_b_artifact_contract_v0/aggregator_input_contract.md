# Aggregator Input Contract

The future aggregator consumes `pocr_stage_b_row_metrics.csv` plus an optional planned denominator manifest.

The aggregator must not read `/tmp` directly. Aggregator must not rely on /tmp replay artifacts.

The aggregator must not infer operation atoms from taxonomy, source SQL, positive SQL, candidate SQL, SQL shape, retained evidence, checker exactness, runtime, or model rationale.

Expected operation atom counts must already be exported from case-local root-level `skills.md` parsing. Semantic guard atoms remain excluded from the operation coverage numerator and denominator.

The aggregator computes macro-average over per-row `oc_i_fail_closed` for each selected denominator view. Macro-average over per-row OC_i is required.

The aggregator may report micro-average only if explicitly requested and labeled diagnostic. Total supported atoms divided by total expected atoms is diagnostic micro-average only.

The aggregator must emit `POCR@curated = NA` and `pocr_curated_status = curated_manifest_missing` unless a predeclared curated manifest exists and is supplied.

The aggregator must preserve boundary columns:

- `diagnostic_only`
- `official_pocr_computed`
- `route_level_pocr_aggregated`
- `paper_metric_promoted`

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
