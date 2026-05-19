# Wave A Common-core v2 Conversion Summary

Task: `case_package_v2_common_core40_wave_a_v0`

Branch: `feature/case-package-v2-external-schema`

## Purpose and Scope

This bounded writable task converted exactly five Common-core Wave A PERF/TPC-H cases to the accepted clean-template-minimal v2 shape:

- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`

The accepted pilot cases used as canonical shape references were `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.

## Folder-order Conversion Summary

Conversion followed the accepted folder order: manifest -> sql -> schema -> checker -> validation -> witness -> evidence_policy -> metadata -> notes -> runs -> README/validator.

All five Wave A cases now have clean case-local v2 assets only:

- `README.md`
- `manifest.yaml`
- `sql/source.sql`
- `sql/pos_01.sql`
- `sql/neg_01.sql`
- `schema/schema_profile.yaml`
- `checker/checker.yaml`
- `checker/normalization.yaml`
- `checker/compare_config.yaml`
- `checker/expected_rejections.yaml`
- `validation/run_validation.sh`
- `validation/run_plan_collection.sh`
- `witness/witness_profile.yaml`

Static evidence is represented by regeneration-first `evidence_policy`, not by committed static evidence paths.

## Schema ID Decisions

The plan originally proposed evaluating a grouped TPC-H schema. The Wave A case-local DDL/load assets differ by case, so a single grouped schema would silently merge incompatible source-of-truth assets. The conversion therefore created case-specific external schema packages:

- `PERF_0008` -> `tpch_perf0008_v0`
- `PERF_0013` -> `tpch_perf0013_v0`
- `PERF_0017` -> `tpch_perf0017_v0`
- `PERF_0019` -> `tpch_perf0019_v0`
- `PERF_0024` -> `tpch_perf0024_v0`

Each package contains `schema_profile.yaml` plus PostgreSQL, MySQL, and Spark `ddl.sql`/`load.sql` copied from the verified case-local assets before deletion of the case-local engine directories.

## Manifest Consistency Summary

All five manifests use the canonical accepted v2 shape:

- direct SQL path lists under `sql.positives` and `sql.negatives`
- profile-first `schema_ref` with `schema_id` and external `profile`
- canonical checker refs
- canonical validation refs
- source-as-oracle witness policy
- regeneration-first `evidence_policy`
- no `evidence_ref`
- no `schema_ref.engines` as current source of truth
- no live references to deleted compatibility directories

## Deleted Compatibility Paths Summary

Deleted for each converted case after static validator pass:

- nested SQL compatibility directories: `sql/positives/`, `sql/negatives/`
- case-local executable schema engine directories: `schema/postgres/`, `schema/mysql/`, `schema/spark/`
- static case evidence: `evidence/`
- metadata compatibility: `metadata/`
- static notes: `notes/`
- data compatibility: `data/`
- old engine-specific validation scripts

No top-level `evidence/cases/` packages were created.

## Deferred or Manual Review Cases

No Wave A case was deferred. No manual-review blocker remains for these five cases.

## Protected Boundary Summary

Protected surfaces unchanged:

- pilot cases unchanged
- `case_sets/` unchanged
- inventory unchanged
- reports/results unchanged
- denominator unchanged
- paper results unchanged
- official metrics computed: no
- DB/checker execution run: no
- global leaderboard created: no
- top-level evidence/cases created: no

## Exact Next Safe Action

Run a bounded Wave A post-conversion parity review, then plan Wave B schema-grouped conversion if the five Wave A cases remain clean-template-minimal and all protected boundaries remain unchanged.
