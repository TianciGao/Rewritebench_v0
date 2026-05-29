# Folder-ordered v2 Conversion Pilot Summary

Task: `case_package_v2_folder_ordered_conversion_pilot_v0`

Branch: `feature/case-package-v2-external-schema`

## Purpose and Scope

This branch-only writable pilot converted only the first three v2 asset layers:

1. `manifest`
2. `sql`
3. `schema`

Pilot case IDs:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

No checker, validation, witness, evidence, metadata, notes, runs cleanup, DB/checker execution, official metrics, paper rendering, reports/results migration, denominator update, `case_sets/` update, or leaderboard output was performed.

## Cases Converted

All five pilot cases were converted for the manifest, direct SQL path, and schema profile/external schema layers.

Cases deferred: none.

## Schema ID Decisions

- `PERF_0006`: reused `tpch_common_core_v0`.
- `PERF_0007`: created `tpch_perf0007_v0` because its DDL/load differ from `tpch_common_core_v0`.
- `CONS_0005`: created `calcite_core_sql_tests_cons0005_v0`.
- `PORT_0003`: created `parrot_bird_port0003_v0`.
- `LONGTAIL_0011`: created `sqlstorm_stackoverflow_longtail0011_v0`.

## SQL Path Conversion Summary

Each pilot case now has:

- `sql/source.sql`
- `sql/pos_01.sql`
- `sql/neg_01.sql`

Existing nested compatibility paths under `sql/positives/` and `sql/negatives/` were not deleted.

## Schema Profile Creation Summary

Each pilot case now has a profile-only case-local schema file at:

- `schema/schema_profile.yaml`

The case-local profile records `schema_id`, external schema profile linkage, source family, relevant tables, columns, column types, primary keys, foreign keys, dialect differences, engine support, and fixture notes.

## External Schema Copy-first Summary

Executable DDL/load files remain external under `schemas/<SCHEMA_ID>/<engine>/`.

Case-local per-engine schema files were retained as compatibility copies. No case-local schema engine files were deleted.

## Validation Summary

Manifest/SQL/schema sanity checks passed for all five pilot cases.

The current `scripts/dev/validate_case_package_v2_refs.py` validator reports `overall_status=fail` for converted cases because it still requires `schema_ref.engines.<engine>.ddl/load`; this task intentionally converted manifests to profile-first `schema_ref` with only `schema_id` and `profile`. For `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`, the validator also reports missing canonical validation wrappers because validation conversion is explicitly out of scope for this task.

`PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v` ran and failed only the `PERF_0006` read-only validator status assertion for the same profile-first `schema_ref` compatibility gap.

No source/test/validator code was modified because it is outside this task's allowed write set.

## Protected Boundary Summary

- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.
- Case-local runs deleted: no.
- Evidence deleted: no.
- Checker/validation/witness/evidence/metadata/notes/runs directories converted: no.
- Legacy repo modified: no.

## Exact Next Safe Action

Authorize `case_package_v2_profile_first_validator_compatibility_v0` to update the static v2 resolver/tests so profile-first `schema_ref` resolves executable engine DDL/load through `schemas/<SCHEMA_ID>/schema_profile.yaml`, then authorize the checker/validation layer pilot.
