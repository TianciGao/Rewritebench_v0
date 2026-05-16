# PERF_0006 Canonical-Layout Migration Plan

Date: 2026-05-16

## Scope

This is a planning-only dry run for a future `PERF_0006` canonical-layout full case migration. No case files were copied, moved, deleted, sanitized, or regenerated in this task. The legacy repository was inspected read-only.

`PERF_0006` is selected after `PORT_0004`, `PORT_0008`, and `CONS_0005` because it tests the canonical layout against a performance-sensitive analytical rewrite case. The prior pilots covered copy-first mechanics, canonical layout with sanitized Spark retained evidence, and checker-heavy CONS hard-negative semantics. `PERF_0006` adds TPC-H-style aggregation, predicate-boundary rewrite pressure, plan observability, and correctness-gated performance boundaries before any Common-core 40 migration.

## Current Legacy Tree Summary

Legacy case root: `cases/PERF/PERF_0006`

Observed files:

- Root case files: `manifest.yaml`, `source.sql`, `rewrite_pos_01.sql`, `rewrite_neg_01.sql`, `data_profile.json`, and `taxonomy_trial_v0.2.yaml`.
- Analysis files: `analysis/canonical_ast.json`, `analysis/logical_ir.json`, `analysis/logical_physical_map.json`, and `analysis/sql_span_logical_map.json`.
- Provenance files: `provenance/raw_record.json` and `provenance/provenance_notes.txt`.
- Metadata file: `metadata/engine_metadata.yaml`.
- Schema files: `schema/ddl_pg.sql`, `schema/ddl_mysql.sql`, and `schema/ddl_spark.sql`.
- Witness/load files: `validation/pg_witness_data.sql`, `validation/mysql_witness_data.sql`, and `validation/spark_witness_data.sql`.
- Validation/checker assets: `validation/check_results.py`, `validation/check_plan_artifacts.py`, `validation/checker.yaml`, `validation/witness_dataset.yaml`, validation scripts, and PostgreSQL/MySQL plan-collection scripts.
- Retained runs evidence: aggregate `runs/result_check.json`, aggregate `runs/plan_check.json`, PostgreSQL source output and source plan, MySQL/Spark positive and negative outputs, MySQL positive and negative plans, and Spark positive/negative plan text.

No release-repo `cases/PERF/PERF_0006/` candidate directory exists at planning time.

## What PERF_0006 Tests That PORT And CONS Pilots Did Not

`PERF_0006` is a performance-pool analytical rewrite case derived from TPC-H Query 1. It tests whether the canonical layout can package a performance-motivated rewrite without creating new timing or speedup claims.

The positive rewrite isolates the source filter in a derived relation before aggregation. The rewrite pressure is primarily:

- predicate pushdown;
- materialization strategy;
- aggregation-heavy analytical query shape;
- plan observability around scan, filter, aggregate, and sort operators.

The hard negative changes `l_shipdate <= DATE '1998-08-27'` to `l_shipdate < DATE '1998-08-27'`, excluding the cutoff-date witness row. It should be packaged as a checker control, not as a method failure or performance claim.

## Proposed Canonical Target Tree

See `PERF_0006_proposed_canonical_tree.txt` for the concrete target tree. The tree follows `repository_spec/canonical_case_package_layout_v1.md` and keeps raw legacy `runs/` as mapped retained evidence, not as a wholesale public copy.

## Source-To-Target Mapping Summary

- Generate a canonical README because the legacy case has no README.
- Generate canonical `manifest.yaml` from the legacy manifest, provenance, retained evidence, and claim-boundary fields.
- Copy `source.sql`, `rewrite_pos_01.sql`, and `rewrite_neg_01.sql` into `sql/source.sql`, `sql/positives/pos_01.sql`, and `sql/negatives/neg_01.sql`.
- Copy engine DDL files into `schema/<engine>/ddl.sql`.
- Copy witness load files into `schema/<engine>/load.sql`.
- Generate `schema/schema_profile.yaml`, `data/data_profile.yaml`, and `data/witness_profile.yaml` from the DDL, witness SQL, `data_profile.json`, and `validation/witness_dataset.yaml`.
- Generate checker YAML files from `validation/checker.yaml`, `validation/check_results.py`, retained outputs, and the cutoff-date hard-negative semantics.
- Copy or wrap legacy validation assets as legacy validation assets with an output-policy caveat. A Spark plan-collection script is absent and should be generated only if approved later.
- Promote public-safe retained JSON/TSV evidence into `evidence/retained_controls/`, `evidence/retained_plans/`, and `evidence/hard_negative/`.
- Sanitize Spark plan text files before public retention, because they contain `file:/tmp` traces.
- Generate metadata YAML and notes from legacy manifest/provenance/taxonomy plus this migration plan.

## Rewrite Pressure And Performance-Observability Emphasis

`PERF_0006` should be described as a performance-sensitive analytical rewrite case, not a speedup result. The source is a frozen TPC-H Q1 instance. The positive rewrite exposes the filtering relation before aggregation, while the negative changes cutoff semantics and fails correctness.

Future migration should preserve the performance boundary:

- retained plan evidence may show operator shape and predicate differences;
- retained result evidence may show correctness gating;
- timing evidence was not found by static inspection;
- no speedup, latency, throughput, or performance ranking should be created by migration.

## Plan Evidence Strategy

Public-safe plan evidence candidates:

- `runs/plan_check.json`;
- `runs/pg/plans/source.json`;
- `runs/mysql/plans/rewrite_pos_01.json`;
- `runs/mysql/plans/rewrite_neg_01.json`.

Spark plan text files are evidence-bearing but not public-safe as-is:

- `runs/spark/plans/rewrite_pos_01.txt`;
- `runs/spark/plans/rewrite_neg_01.txt`.

They contain local temporary path traces and should be sanitized into `evidence/retained_plans/spark/*.sanitized.txt` or kept private/archive-only. Sanitization must preserve operator names, predicates, aggregates, table names, column names, and plan structure.

## Runs Retention Strategy

Do not delete or mutate legacy `runs/`.

Future migration should:

- copy public-safe retained result-check and TSV evidence into `evidence/retained_controls/` and `evidence/hard_negative/`;
- copy public-safe PostgreSQL and MySQL JSON plan evidence into `evidence/retained_plans/`;
- sanitize Spark plan text files before public retention;
- map every original legacy run artifact in `evidence/runs_retention.yaml` with `do_not_delete_original: true`;
- avoid wholesale public `runs/` publication;
- record that no timing artifact was found and no speedup claim is created.

## Manifest Strategy

The future manifest should be generated, not byte-for-byte copied. It should preserve legacy identity fields and add canonical path fields for SQL, schema, checker, validation, evidence, metadata, notes, and claim boundaries.

Required claim boundaries:

- `denominator_changed: false`
- `paper_results_changed: false`
- `common_core_membership_changed: false`
- `no_global_leaderboard: true`
- `db_validation_run: false`
- `evidence_regenerated: false`
- `speedup_claim_created: false`
- `migration_scope: PERF_0006_only`

## Validator v0.3 Implications

After actual migration, `full-case` and `canonical-case` modes should pass only if:

- SQL is under `sql/`;
- schema/load context exists under `schema/<engine>/`;
- checker YAML exists and parses;
- validation assets are caveated as legacy assets or wrapped;
- retained evidence is mapped and public-safe;
- raw `runs/` is not copied wholesale;
- Spark plans are sanitized or kept out of public retained evidence;
- timing/speedup boundaries remain explicit;
- claim boundaries remain unchanged.

## Public Hygiene Risks

Static precheck found:

- Spark plan text files contain `file:/tmp` and `/tmp/` traces and need sanitization or private/archive mapping.
- No prompt/API/token risk was found by the configured static scan.
- No timing/speedup artifact was found by static file-name/content inspection.

## Risks And Abort Conditions

See:

- `PERF_0006_canonical_migration_risk_register.md`
- `PERF_0006_abort_conditions.md`

The highest-risk item is performance-boundary overclaiming: because this is a PERF case, future migration must not convert retained correctness/plan evidence into a new speedup or leaderboard claim.

## Recommended Actual Migration Sequence

1. Confirm release repo is clean and legacy repo is read-only.
2. Re-run the static public hygiene precheck against the legacy case.
3. Create canonical directory structure under `cases/PERF/PERF_0006/`.
4. Copy SQL, schema, witness load, and approved validation assets using canonical names.
5. Generate manifest, checker YAML, data/schema profiles, metadata YAML, README, and migration notes.
6. Promote public-safe retained JSON/TSV evidence into `evidence/`.
7. Sanitize Spark plan text files or mark them private/archive-only before public retention.
8. Create `evidence/runs_retention.yaml` with explicit no-speedup and do-not-delete mappings.
9. Run YAML/JSON/hygiene validation.
10. Run validator v0.3 in `full-case` and `canonical-case` modes.
11. Commit explicit paths only.

## Boundary Statement

This planning task does not migrate `PERF_0006`. It does not start Common-core 40 migration, change denominators, change paper results, change case membership, create speedup claims, regenerate evidence, execute DB engines, or modify raw legacy evidence.
