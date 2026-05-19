# Common-core 40 Wave B v2 Conversion Summary

## Purpose and Scope

This task converted exactly 22 schema-grouped non-PORT Common-core cases to the accepted clean-template-minimal v2 case shape. The conversion used the five accepted pilot cases and five Wave A cases as canonical examples.

## Converted Case IDs

- PERF: `PERF_0033`, `PERF_0034`, `PERF_0035`, `PERF_0052`, `PERF_0054`, `PERF_0056`, `PERF_0062`, `PERF_0077`, `PERF_0082`
- CONS: `CONS_0007`, `CONS_0009`, `CONS_0010`, `CONS_0011`, `CONS_0012`, `CONS_0024`, `CONS_0036`, `CONS_0037`
- LONGTAIL: `LONGTAIL_0012`, `LONGTAIL_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, `LONGTAIL_0024`

No PORT/manual-review cases, pilot cases, or Wave A cases were modified.

## Folder-Order Conversion Summary

- Manifest: all 22 manifests now use canonical v2 shape with direct SQL lists, profile-first `schema_ref`, config-only checker refs, thin validation wrapper refs, source-as-oracle witness policy, and regeneration-first `evidence_policy`.
- SQL: direct `sql/source.sql`, `sql/pos_01.sql`, and `sql/neg_01.sql` are present for every converted case; nested positive/negative compatibility directories were removed.
- Schema: case-local `schema/schema_profile.yaml` is retained as the case-facing profile; executable DDL/load assets were moved to external schema packages under `schemas/`.
- Checker: checker directories contain YAML configuration only and no per-case Python checker scripts.
- Validation: each case keeps only `run_validation.sh` and `run_plan_collection.sh` thin fail-closed wrappers.
- Witness: each converted case has a lightweight source-as-oracle `witness/witness_profile.yaml`; no static correct-result file was fabricated.
- Evidence policy: static case evidence is not required; no top-level `evidence/cases/` directory was created.
- Cleanup: case-local static evidence, metadata, notes, data, case-local engine schema directories, nested SQL directories, and old engine-specific validation scripts were removed for the 22 target cases.

## Schema ID Decisions

The Wave B planning artifact grouped cases by source family, but exact DDL/load hashing showed 22 distinct schema asset tuples. To avoid unsafe schema reuse, this conversion created one external schema package per case:

- `tpcds_perf0033_v0` for `PERF_0033`
- `tpcds_perf0034_v0` for `PERF_0034`
- `tpcds_perf0035_v0` for `PERF_0035`
- `tpcds_perf0052_v0` for `PERF_0052`
- `tpcds_perf0054_v0` for `PERF_0054`
- `tpcds_perf0056_v0` for `PERF_0056`
- `tpcds_perf0062_v0` for `PERF_0062`
- `job_imdb_perf0077_v0` for `PERF_0077`
- `job_imdb_perf0082_v0` for `PERF_0082`
- `calcite_core_sql_tests_cons0007_v0` for `CONS_0007`
- `calcite_core_sql_tests_cons0009_v0` for `CONS_0009`
- `calcite_core_sql_tests_cons0010_v0` for `CONS_0010`
- `calcite_core_sql_tests_cons0011_v0` for `CONS_0011`
- `calcite_core_sql_tests_cons0012_v0` for `CONS_0012`
- `calcite_core_sql_tests_cons0024_v0` for `CONS_0024`
- `verieql_cons0036_v0` for `CONS_0036`
- `verieql_cons0037_v0` for `CONS_0037`
- `sqlstorm_stackoverflow_longtail0012_v0` for `LONGTAIL_0012`
- `sqlstorm_stackoverflow_longtail0013_v0` for `LONGTAIL_0013`
- `stack_queries_longtail0022_v0` for `LONGTAIL_0022`
- `stack_queries_longtail0023_v0` for `LONGTAIL_0023`
- `stack_queries_longtail0024_v0` for `LONGTAIL_0024`

## Manifest Consistency Summary

All 22 Wave B manifests passed the strict consistency audit. No converted manifest requires `evidence_ref`, static evidence paths, case-local run paths, nested SQL paths, case-local engine schema paths, old validation scripts, absolute paths, or local machine paths.

## Deleted Compatibility Paths Summary

The cleanup manifest records 330 high-level deletion entries: 44 nested SQL directory entries, 66 case-local engine schema directory entries, 88 case-local evidence/metadata/notes/data directory entries, and 132 old engine-specific validation script entries. Deletions were limited to the 22 Wave B case packages.

## Deferred or Manual Review Cases

None. All 22 Wave B cases converted and passed static validation.

## Protected Boundary Summary

No `case_sets/`, inventory, reports, results, denominator values, paper results, official metrics, DB/checker execution, global leaderboard output, PORT manual-review cases, pilot cases, or Wave A cases were modified. No `evidence/cases/` surfaces were created.

## Exact Next Safe Action

Run `case_package_v2_common_core40_wave_b_post_conversion_review_v0` as a read-only parity review over the 22 converted Wave B cases plus the accepted pilot and Wave A cases before authorizing Wave C/manual-review PORT conversion.
