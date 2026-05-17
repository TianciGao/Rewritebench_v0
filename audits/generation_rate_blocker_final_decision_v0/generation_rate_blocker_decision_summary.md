# Generation Rate Blocker Final Decision v0

## Purpose And Scope

This decision packet resolves the public v0 treatment of Generation Rate for the A-line metric-readiness closure sequence.

No Generation Rate was computed. No official metrics were computed or recomputed. No paper tables were rendered. No `reports/` or `results/` files were created or updated. Denominator values, paper results, case membership, candidate ledgers, inference overlays, and raw legacy evidence were unchanged.

## Current Blocker

Generation Rate remains blocked by:

`inferred_generated_policy_not_official_and_sqlglot_generated_ready_gap`

Metrics Contract v1 defines Generation Rate as emitted candidate SQL over planned candidate cases. The current evidence chain has observed generated evidence for only part of the non-SQLGlot routes, 94 audit-only `inferred_generated=true` rows derived from `ready=true`, and no source-observed generated/ready evidence for the SQLGlot parser v1 rows.

## Evidence Reviewed

- `official_status_metrics_v0_limited` computed only Execution Coverage Rate and Result Consistency Rate.
- `official_status_metrics_v0_limited` explicitly blocked Generation Rate and wrote no official Generation Rate values.
- `status_inference_policy_v0` identified 94 potential R1 ready-implies-generated rows and 0 exact-implies-executed rows.
- `status_inference_overlay_v0` materialized 94 audit-only inferred rows without overwriting observed fields.
- `normalized_status_only_metrics_dryrun_v4` used inferred generated only for audit dry-run logic.
- `combined_candidate_status_overlay_v2` contains 312 filled rows and 288 unresolved rows, but SQLGlot generated/ready evidence remains unavailable.
- `A_line_final_metrics_closure_plan_v0` recommended this task before renderer input packaging.

## Options Reviewed

Option A keeps Generation Rate blocked until observed generated evidence improves. This is the safest primary v0 treatment because it preserves the Metrics Contract v1 meaning of emitted candidate SQL.

Option B officializes `inferred_generated` with strict labeling. This is not recommended for v0 because ready semantics remain policy-sensitive and SQLGlot generated/ready evidence is still missing.

Option C creates a diagnostic Generation/Readiness support table, not a primary official metric. This is useful as a future support artifact only if separately authorized and clearly labeled as non-primary and non-paper.

Option D defers Generation Rate to post-release. This is safe but less informative than reporting the v0 blocker explicitly.

## Recommended v0 Treatment

Generation Rate should be reported as blocked for public v0. It should not be officialized from inferred-generated evidence. A future diagnostic Generation/Readiness support table may be planned separately, but it must not be treated as the primary Generation Rate metric or a paper result.

## Why No Generation Rate Was Computed

The numerator would require source-observed emitted candidate SQL evidence or a separately authorized policy that allows inference into official metric input. Neither condition is satisfied for v0. Inferred-generated rows remain audit-only, and SQLGlot generated/ready evidence is incomplete.

## Paper And Report Implication

Future paper or report renderers must display Generation Rate as blocked or diagnostic-only, not as an official primary metric. Any renderer input package must keep Execution Coverage Rate and Result Consistency Rate separate from the blocked Generation Rate row and must preserve denominator partitions and the no-global-leaderboard guard.

## Exact Next Safe Action

Run `non_status_metric_na_backlog_closure_bundle_v0` to close Semantic Equivalence, performance, attribution, cross-engine, and Speedup Retention as blocked, N.A., or post-release without implementing adapters, computing metrics, rendering paper tables, or writing reports/results.
