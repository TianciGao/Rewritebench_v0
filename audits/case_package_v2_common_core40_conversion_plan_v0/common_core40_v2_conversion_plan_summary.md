# Common-core 40 v2 Conversion Plan Summary

Task: `case_package_v2_common_core40_conversion_plan_v0`

Branch: `feature/case-package-v2-external-schema`

## Purpose and Scope

This branch-only read-only plan uses the accepted five-case clean-template-minimal v2 pilot as the template for planning full Common-core 40 conversion.

Accepted pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

This task did not modify case packages, schemas, evidence, `case_sets/`, inventory, reports/results, denominator values, paper results, or execution outputs. No DB/checker execution or official metric computation was run.

## Pilot Gate Used

The plan uses the post-evidence-removal pilot acceptance gate:

- functional v2 accepted
- clean-template-minimal achieved
- static evidence is not required for clean v2
- `evidence_policy` replaces mandatory `evidence_ref`
- case-local placeholder `runs/` directories were removed earlier
- only `PORT_0003/sql/dialect_variants/` remains as an optional semantic v2 asset
- protected benchmark surfaces remain unchanged

## Common-core 40 Review Result

Reviewed Common-core cases: 40.

Readiness distribution:

- already converted pilot: 5
- Wave A auto clean-template conversion: 5
- Wave B schema-grouped conversion: 22
- Wave C/manual schema or dialect review: 1
- blocked manual review: 7

The 35 non-pilot cases are currently canonical v1-style packages, not clean-template-minimal v2 packages. They generally still use nested SQL positive/negative paths, case-local schema engine directories, static evidence sections, metadata/data/notes directories, and old engine-specific validation scripts.

## Planned Waves

Future writable conversion should use three waves after the pilot gate.

Wave A: 5 TPC-H non-pilot PERF cases.

- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`

These are the lowest-risk next cases because they share the PERF/TPC-H conversion pattern and do not require PORT dialect review.

Wave B: 22 schema-grouped non-PORT cases.

- TPC-DS PERF cases: `PERF_0033`, `PERF_0034`, `PERF_0035`, `PERF_0052`, `PERF_0054`, `PERF_0056`, `PERF_0062`
- JOB/IMDB PERF cases: `PERF_0077`, `PERF_0082`
- CONS Calcite cases: `CONS_0007`, `CONS_0009`, `CONS_0010`, `CONS_0011`, `CONS_0012`, `CONS_0024`
- CONS VeriEQL cases: `CONS_0036`, `CONS_0037`
- LONGTAIL SQLStorm cases: `LONGTAIL_0012`, `LONGTAIL_0013`
- LONGTAIL Stack Queries cases: `LONGTAIL_0022`, `LONGTAIL_0023`, `LONGTAIL_0024`

Wave C/manual review: 8 PORT cases.

- `PORT_0005` needs manual schema/dialect review before conversion.
- `PORT_0004`, `PORT_0008`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025` remain D008-blocked until manual-review resolution.

## Folder-Ordered Plan

Every writable wave should follow:

`manifest -> sql -> schema -> checker -> validation -> witness -> evidence_policy -> metadata -> notes -> runs -> README/validator`

The five pilot cases showed this sequence can converge to clean-template-minimal while preserving denominator, paper, report/result, and leaderboard boundaries.

## Schema Strategy

Existing pilot schemas remain as accepted:

- `tpch_common_core_v0`
- `tpch_perf0007_v0`
- `calcite_core_sql_tests_cons0005_v0`
- `parrot_bird_port0003_v0`
- `sqlstorm_stackoverflow_longtail0011_v0`

Future conversion should create or extend grouped schemas only after verifying the case-local engine DDL/load assets:

- `tpch_common_core40_v0`
- `tpcds_common_core40_v0`
- `job_imdb_common_core40_v0`
- `calcite_core_sql_tests_common_core40_v0`
- `verieql_cons_common_core40_v0`
- `sqlstorm_stackoverflow_common_core40_v0`
- `stack_queries_longtail_common_core40_v0`

PORT cases should use per-case or manually reviewed schema packages after dialect review.

## Evidence Policy

All future converted Common-core cases should use:

```yaml
evidence_policy:
  static_case_evidence: not_required
  regeneration_policy: regenerable_by_validation_and_report_scripts
  retained_static_artifacts: none
```

Static case-local evidence and top-level `evidence/cases/` packages are not required final clean v2 public surfaces. Reports/results remain separately authorized surfaces and must not be modified by conversion waves.

## Manual Review Blockers

The PORT manual-review set is the only blocker group before full Common-core 40 clean-template-minimal completion. D008 remains active for:

- `PORT_0004`
- `PORT_0008`
- `PORT_0012`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

`PORT_0005` is not D008-blocked, but should still be handled in Wave C because it requires dialect/schema review.

## Protected Boundary Summary

Protected surfaces unchanged:

- case files modified: no
- schemas modified: no
- evidence modified: no
- runs deleted: no
- `case_sets/` changed: no
- inventory changed: no
- reports/results changed: no
- denominator changed: no
- paper results changed: no
- official metrics computed: no
- DB/checker execution run: no
- global leaderboard created: no

## Exact Next Safe Action

Authorize `case_package_v2_common_core40_wave_a_v0` as a bounded writable Wave A conversion for only `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, and `PERF_0024`, using the accepted pilot template and preserving all protected benchmark surfaces.
