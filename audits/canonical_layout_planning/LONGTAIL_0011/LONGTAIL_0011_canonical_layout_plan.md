# LONGTAIL_0011 Canonical-Layout Migration Plan

Date: 2026-05-16

Planning status: planning only. No case files were copied, moved, generated under `cases/`, or migrated by this task.

## Purpose

`LONGTAIL_0011` is proposed as the next single-case canonical-layout migration candidate after:

- `PORT_0004`, which tested legacy-compatible copy-first migration.
- `PORT_0008`, which tested canonical layout and sanitized retained evidence integration.
- `CONS_0005`, which tested checker-heavy hard-negative packaging.
- `PERF_0006`, which tested performance-sensitive analytical packaging without creating new speedup claims.

`LONGTAIL_0011` should test whether the canonical public-release package layout works for realistic, structurally complex, long-tail SQL. This planning task does not start Common-core 40 migration, does not modify denominators or paper results, and does not alter raw legacy evidence.

## Current Legacy Tree Summary

Legacy case root inspected read-only: `cases/LONGTAIL/LONGTAIL_0011/`

Important files present:

- Root files: `README.md`, `manifest.yaml`, `source.sql`, `rewrite_pos_01.sql`, `rewrite_neg_01.sql`, `risk_notes.md`, `witness_design_notes.md`, `schema_notes.md`, `promotion_checklist.md`.
- Schema files: `schema/ddl_pg.sql`, `schema/ddl_mysql.sql`, `schema/ddl_spark.sql`.
- Witness/load files: `validation/pg_witness_data.sql`, `validation/mysql_witness_data.sql`, `validation/spark_witness_data.sql`.
- Validation scripts: PostgreSQL, MySQL, and Spark witness validation and plan collection scripts.
- Retained run evidence: PostgreSQL, MySQL, and Spark result TSVs, `result_check.json` summaries, plan artifacts, and `plan_check.json` summaries.
- Missing legacy package components for canonical layout: no `metadata/`, no `checker/`, no case-local `evidence/runs_retention.yaml`, no canonical `sql/` layout, and no canonical public `evidence/` layout.

Legacy manifest identity:

- `case_id`: `LONGTAIL_0011`
- `primary_pool`: `longtail`
- `source_family`: `SQLStorm`
- `source_workload`: `stackoverflow`
- `source_query_identity`: `6625.sql`
- `draft_origin`: `LONGTAIL_DRAFT_0012`
- `official_case_status`: `case_local_constructed_not_registry_admitted`

## Proposed Canonical Target Tree

Future actual migration should create the canonical release package under:

`cases/LONGTAIL/LONGTAIL_0011/`

The proposed tree is recorded in `LONGTAIL_0011_proposed_canonical_tree.txt`. It follows `repository_spec/canonical_case_package_layout_v1.md` and keeps raw legacy `runs/` mapped rather than copied wholesale.

## Source-To-Target Mapping Summary

The full row-level mapping is recorded in `LONGTAIL_0011_canonical_file_mapping.csv`.

Key future mappings:

- `source.sql` -> `sql/source.sql`
- `rewrite_pos_01.sql` -> `sql/positives/pos_01.sql`
- `rewrite_neg_01.sql` -> `sql/negatives/neg_01.sql`
- `schema/ddl_pg.sql` -> `schema/postgres/ddl.sql`
- `schema/ddl_mysql.sql` -> `schema/mysql/ddl.sql`
- `schema/ddl_spark.sql` -> `schema/spark/ddl.sql`
- `validation/pg_witness_data.sql` -> `schema/postgres/load.sql`
- `validation/mysql_witness_data.sql` -> `schema/mysql/load.sql`
- `validation/spark_witness_data.sql` -> `schema/spark/load.sql`
- `runs/*/result_check.json` and public-safe TSV outputs -> `evidence/retained_controls/`
- negative TSV outputs and hard-negative summary -> `evidence/hard_negative/`
- PostgreSQL and MySQL JSON plans -> `evidence/retained_plans/postgres/` and `evidence/retained_plans/mysql/`
- Spark plan text -> sanitize before public copy under `evidence/retained_plans/spark/`
- raw legacy `runs/` -> reference-only/archive mapping through `evidence/runs_retention.yaml`

## Long-Tail Structure And Robustness Emphasis

`LONGTAIL_0011` is structurally different from prior pilots:

- It is SQLStorm-derived from the StackOverflow workload line.
- It uses a CTE pipeline: `RankedPosts` and `MaxRank` in the source.
- It uses window functions: `DENSE_RANK()` in the source and positive rewrite.
- It uses joins between `Posts` and `Users`.
- It uses ordering, filtering, grouping, and realistic multi-clause query shape.
- It stresses tie-handling semantics for per-user worst-question selection.

The long-tail label should be represented as a structural characterization only. Migration must not create a workload-frequency, production-frequency, broad-coverage, or global-leaderboard claim.

## Correctness And Hard Negative

Static evidence supports a hard-negative boundary:

- `source.sql` ranks posts per owner using `DENSE_RANK()` and then selects the maximum descending rank per user.
- `rewrite_pos_01.sql` uses `DENSE_RANK()` ascending and selects `WorstRank = 1`.
- `rewrite_neg_01.sql` changes the rank function to `ROW_NUMBER()` ascending.
- The witness has two tied worst Alice rows with equal score.
- Source and positive outputs include both tied Alice rows.
- The negative output collapses the tied Alice rows and returns only one of them.

Future `checker/expected_rejections.yaml` should encode `tie_handling_semantics_changed` or equivalent, with a human-review note before the actual migration if maintainers want the exact canonical reason string approved.

## Plan Evidence Strategy

PostgreSQL and MySQL JSON plan artifacts appear suitable for public retained plan evidence after normal hygiene and JSON parsing checks.

Spark plan text files contain local temporary path traces such as `file:/tmp/...` and must not be copied raw into public retained evidence. Future migration should either:

- create sanitized public copies under `evidence/retained_plans/spark/`, replacing local temporary paths with `<LOCAL_TMP_PATH_REDACTED>`, or
- leave raw Spark plan text private/archive-only and map it through `evidence/runs_retention.yaml`.

The preferred action is sanitize-before-public-copy, preserving Spark plan structure, operator names, table names, column names, expressions, and plan semantics.

## runs/ Retention Strategy

Future actual migration must not copy raw `runs/` wholesale into the public canonical package. It should:

- promote public-safe result summaries and TSV outputs to `evidence/retained_controls/`;
- promote hard-negative TSV outputs and a generated hard-negative summary to `evidence/hard_negative/`;
- promote public-safe PostgreSQL/MySQL plan JSONs to `evidence/retained_plans/`;
- sanitize Spark plan text before public release, or map it as private/archive-only;
- map all original legacy run artifacts with `do_not_delete_original: true`;
- explicitly state raw legacy evidence was not changed.

## Manifest Strategy

Future actual migration should generate a canonical `manifest.yaml` from the legacy manifest, this plan, retained evidence, and generated metadata. It should not byte-copy the legacy manifest as final public manifest.

The manifest must preserve:

- `case_id: LONGTAIL_0011`
- `pool: LONGTAIL`
- `migration_scope: LONGTAIL_0011_only`
- `canonical_layout: true`
- `denominator_changed: false`
- `paper_results_changed: false`
- `common_core_membership_changed: false`
- `no_global_leaderboard: true`
- `db_validation_run: false`
- `evidence_regenerated: false`
- `workload_frequency_claim_created: false`

## Validator v0.3 Implications

Expected current state:

- No release `cases/LONGTAIL/LONGTAIL_0011/` package exists.
- The current legacy-compatible layout would not satisfy canonical-case mode without canonical package creation.

Expected after actual migration:

- `full-case` mode should pass if all required structure, metadata, runs-retention, evidence mapping, hygiene, and claim-boundary checks pass.
- `canonical-case` mode should pass only if the canonical layout is created, Spark plan traces are sanitized or not published, validation script caveats are explicit, and raw `runs/` is not copied wholesale.

## Public Hygiene Risks

Static precheck found:

- Spark plan text files contain `file:/tmp` local temporary path traces.
- Spark validation and plan-collection scripts contain WSL-local wording in comments.

Future migration must sanitize or avoid publishing those Spark plan text files raw, and must adapt Spark script comments or add clear output-policy caveats.

## Risks And Abort Conditions

The detailed risk register is in `LONGTAIL_0011_canonical_migration_risk_register.md`.

The actual migration must abort if:

- release repo is dirty at start;
- legacy case files are missing;
- public hygiene scan fails after proposed sanitization/adaptation;
- copied-file SHA256 validation fails for copy-as-is files;
- manifest and runs-retention claims conflict;
- hard-negative expected rejection reason is not accepted for release packaging;
- validator v0.3 `full-case` or `canonical-case` fails;
- denominator, paper results, membership, or raw legacy evidence would change.

## Recommended Actual Migration Sequence

1. Start from a clean release repo and inspect legacy repo read-only.
2. Confirm no existing release `cases/LONGTAIL/LONGTAIL_0011/` package exists, or that any existing path is an abandoned attempt approved for replacement.
3. Create canonical directories under `cases/LONGTAIL/LONGTAIL_0011/`.
4. Copy SQL, schema, witness/load, selected notes, validation assets, and public-safe retained evidence according to the mapping CSV.
5. Generate README, canonical manifest, schema/data profiles, checker YAML, expected-rejections YAML, metadata YAML, package summary JSON, migration notes, and runs-retention YAML.
6. Sanitize Spark plan text before public retained evidence publication, or map raw Spark plans as private/archive-only.
7. Run SHA256 copy validation, public hygiene scan, YAML parse, JSON parse, validator v0.3 full-case, validator v0.3 canonical-case, evidence-pilot regression, full-case regression, py_compile, and git checks.
8. Commit explicit paths only.

## Planning Boundary

This task creates only planning/audit files under `audits/canonical_layout_planning/LONGTAIL_0011/` and project-control writeback. It does not migrate `LONGTAIL_0011`, does not create `cases/LONGTAIL/LONGTAIL_0011/`, does not change case membership, and does not modify the legacy repo.
