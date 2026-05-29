# Wave A Post-Conversion Parity Review Summary

Task: `case_package_v2_common_core40_wave_a_post_conversion_parity_review_v0`

Branch: `feature/case-package-v2-external-schema`

## Purpose and Scope

This branch-only read-only review rechecked exactly the five Common-core Wave A cases converted by `case_package_v2_common_core40_wave_a_v0`:

- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`

It also rechecked the accepted pilot cases for validator non-regression:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

This review did not modify case packages, schemas, `case_sets/`, inventory, reports/results, denominators, paper results, metric outputs, DB/checker outputs, or leaderboard outputs.

## Validation Result

All five Wave A cases passed the static v2 validator. All five accepted pilot cases also passed the static v2 validator. The `tests/case_package_v2` unittest suite passed with 11 tests.

No DB/checker execution was run and no official metrics were computed.

## Manifest Consistency

All five Wave A manifests match the accepted canonical v2 core shape:

- direct SQL refs: `sql/source.sql`, `sql/pos_01.sql`, `sql/neg_01.sql`
- profile-first `schema_ref` with `schema_id` and external `profile`
- canonical checker config refs
- canonical validation wrapper refs
- source-as-oracle witness policy
- regeneration-first `evidence_policy`
- no mandatory `evidence_ref`
- no manifest refs to deleted nested SQL, case-local evidence, case-local runs, case-local engine schema dirs, or old engine validation scripts

## Clean-Template-Minimal Result

All five Wave A cases satisfy the clean-template-minimal case-local structure:

```text
README.md
manifest.yaml
sql/source.sql
sql/pos_01.sql
sql/neg_01.sql
schema/schema_profile.yaml
checker/checker.yaml
checker/normalization.yaml
checker/compare_config.yaml
checker/expected_rejections.yaml
validation/run_validation.sh
validation/run_plan_collection.sh
witness/witness_profile.yaml
```

No Wave A case-local compatibility gap remains. The forbidden case-local surfaces are absent for all five Wave A cases: `evidence/`, `runs/`, `metadata/`, `notes/`, `data/`, `schema/postgres/`, `schema/mysql/`, `schema/spark/`, nested SQL positive/negative dirs, old engine-specific validation scripts, per-case Python checker scripts, `run_engine_queries.py`, and `__pycache__/`.

The validation wrappers still contain fail-closed guards that refuse case-local `runs/` output. These are policy guards, not live dependencies on a retained `runs/` directory.

## Schema Policy Recheck

Each Wave A case uses a case-specific external schema package because the conversion task verified that the DDL/load assets differed by case:

- `PERF_0008` -> `tpch_perf0008_v0`
- `PERF_0013` -> `tpch_perf0013_v0`
- `PERF_0017` -> `tpch_perf0017_v0`
- `PERF_0019` -> `tpch_perf0019_v0`
- `PERF_0024` -> `tpch_perf0024_v0`

For each case, the case-local `schema/schema_profile.yaml` exists, `manifest.schema_ref.profile` resolves, the external schema profile exists, and PostgreSQL/MySQL/Spark DDL/load refs in the external profile resolve.

## Protected Boundary Summary

Protected surfaces unchanged:

- case files modified by this review: no
- schemas modified by this review: no
- `case_sets/` changed: no
- inventory changed: no
- reports/results changed: no
- denominator changed: no
- paper results changed: no
- official metrics computed: no
- DB/checker execution run: no
- global leaderboard created: no

## Conclusion

Wave A post-conversion parity passed. The five Wave A cases are clean-template-minimal v2 cases, their manifests remain consistent with the accepted pilot shape, and no Wave A cleanup gap remains.

Ready for Wave B: yes, as a bounded conversion of the schema-grouped non-PORT Wave B cases only.

## Exact Next Safe Action

Authorize a bounded `case_package_v2_common_core40_wave_b_v0` conversion for schema-grouped non-PORT cases only. Do not include Wave C/PORT manual-review cases, do not run DB/checker execution, and do not modify protected benchmark surfaces.
