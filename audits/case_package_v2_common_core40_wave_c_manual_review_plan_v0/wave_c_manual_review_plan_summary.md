# Common-core 40 Wave C Manual-Review Plan v0

## Purpose and scope

This branch-only read-only plan identifies the remaining Common-core v2 conversion work after the accepted five-case pilot, Wave A, Wave B, manifest semantic-contract repair, and manifest caveat closeout. It does not perform writable conversion, PORT conversion execution, DB/checker execution, official metric computation, reports/results migration, denominator updates, case-set updates, inventory updates, or leaderboard creation.

## Wave C case list

Authoritative sources agree that the remaining Common-core cases are eight PORT/manual-review cases:

- `PORT_0004`
- `PORT_0005`
- `PORT_0008`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

The final list was cross-checked against `common_core40_conversion_waves.csv`, `common_core40_manual_review_blockers.csv`, `common_core40_v2_case_readiness.csv`, and `case_sets/common_core_v0/cases.csv`. The set also equals the Common-core case set minus the 32 already converted/repaired v2 cases.

## Why this is planning only

All eight cases still use the pre-v2/canonical compatibility shape: nested `sql/positives/` and `sql/negatives/`, case-local schema engine directories, case-local evidence, metadata, notes, data, and legacy engine-specific validation scripts. External schema packages for the proposed Wave C schema ids are absent. Seven cases remain D008-blocked, and `PORT_0005` still needs an explicit dialect/schema decision.

## Readiness classification

- Ready for bounded conversion now: 0.
- Ready after manifest-only review: 0.
- Ready after dialect/schema review: 1 (`PORT_0005`).
- Deferred pending D008 manual review: 7 (`PORT_0004`, `PORT_0008`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0024`, `PORT_0025`).

## Dialect / PORT risk summary

`PORT_0004`, `PORT_0005`, and `PORT_0013` currently contain Spark dialect-variant SQL under `sql/dialect_variants/spark/`. Future conversion must preserve those variants unless a manual portability review explicitly proves they are stale. The other five Wave C cases do not currently contain dialect-variant directories, but D008 still requires public-safety and retained-artifact review before conversion.

## Schema strategy

Use per-case external schema packages, not a silent shared schema id. The proposed ids are `parrot_bird_port0004_v0`, `parrot_bird_port0005_v0`, `parrot_bird_port0008_v0`, `parrot_bird_port0012_v0`, `parrot_bird_port0013_v0`, `parrot_bird_port0022_v0`, `parrot_bird_port0024_v0`, and `parrot_bird_port0025_v0`. Each future execution must verify/copy DDL and load files before deleting case-local `schema/<engine>/` directories.

## Manifest risk summary

All eight manifests need colleague-style semantic v2 conversion. Source-family and source-entry pointers are present, taxonomy metadata exists, and nested positive/hard-negative SQL can be mapped, but future manifests must not invent source fields, draft origins, taxonomy, or dialect semantics. Draft origin should be explicit where available or retained as an explicit caveat/fallback where not recoverable.

## Recommended Wave C execution split

Do not convert all eight in one blind writable batch. Recommended sequence:

1. Run a read-only Wave C preclearance packet for D008 and dialect/schema decisions.
2. Convert `PORT_0005` alone after dialect/schema approval.
3. Convert D008-cleared cases without current dialect variants: `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
4. Convert D008-cleared cases with current dialect variants: `PORT_0004` and `PORT_0013`, preserving variants when semantically needed.

## PERF_0077/PERF_0082 separate caveat follow-up

`PERF_0077` and `PERF_0082` remain already converted Wave B cases with `source_path_not_recovered` caveats. These caveats do not block Wave C planning, but they require a separate narrow provenance follow-up before final public source-path closeout.

## Protected boundary summary

No case packages, schemas, `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker execution, or leaderboard outputs were modified or produced.

## Exact next safe action

Authorize a read-only `case_package_v2_common_core40_wave_c_preclearance_v0` packet to resolve D008 public-safety/dialect/schema decisions for the eight PORT cases before any writable Wave C conversion execution.
