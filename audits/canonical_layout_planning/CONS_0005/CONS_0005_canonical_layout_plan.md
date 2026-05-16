# CONS_0005 Canonical-Layout Migration Plan

Date: 2026-05-16

## Scope

This is a planning-only dry run for a future `CONS_0005` canonical-layout full case migration. No case files were copied, moved, deleted, sanitized, or regenerated in this task. The legacy repository was inspected read-only.

`CONS_0005` is selected after `PORT_0004` and `PORT_0008` because it tests the canonical layout against a CONS case whose central value is checker-heavy hard-negative behavior: correlated `NOT IN`, NULL semantics, anti-join semantics, witness rows, and expected rejection evidence. `PORT_0004` tested copy-first full migration in a legacy-compatible layout. `PORT_0008` tested canonical layout plus sanitized retained Spark plan integration. `CONS_0005` should test canonical checker, expected-rejection, witness-profile, and hard-negative packaging across pools before any Common-core 40 migration.

## Current Legacy Tree Summary

Legacy case root: `cases/CONS/CONS_0005`

Observed files:

- Root case files: `README.md`, `manifest.yaml`, `source.sql`, `rewrite_pos_01.sql`, `rewrite_neg_01.sql`, `risk_notes.md`, `witness_design_notes.md`, `schema_notes.md`, `promotion_checklist.md`.
- Schema files: `schema/ddl_pg.sql`, `schema/ddl_mysql.sql`, `schema/ddl_spark.sql`.
- Witness/load files: `validation/pg_witness_data.sql`, `validation/mysql_witness_data.sql`, `validation/spark_witness_data.sql`.
- Validation/checker assets: `validation/check_results.py`, `validation/check_plan_artifacts.py`, three validation scripts, and three plan-collection scripts.
- Retained run evidence: per-engine `result_check.json`, per-engine output TSVs, per-engine plan artifacts, aggregate `runs/result_check.json`, and aggregate `runs/plan_check.json`.

There is no release-repo `cases/CONS/CONS_0005/` candidate directory at planning time.

## What CONS_0005 Tests That PORT Pilots Did Not

- CONS hard-negative handling: source and positive rewrite produce no rows, while the negative rewrite produces `1\t3` on the retained witness.
- Checker semantics: the future checker must preserve `source == positive` and `source != negative` across PostgreSQL, MySQL, and Spark without claiming admission or leaderboard results.
- Expected rejections: `checker/expected_rejections.yaml` must encode why `rewrite_neg_01.sql` is intentionally rejected.
- Witness packaging: small NULL-bearing witness rows must be represented in `schema/<engine>/load.sql`, `data/data_profile.yaml`, and `data/witness_profile.yaml`.
- Spark plan hygiene: retained Spark plan text files contain `file:/tmp` traces and require future sanitization before public retained evidence promotion.

## Proposed Canonical Target Tree

See `CONS_0005_proposed_canonical_tree.txt` for the concrete target tree. The target follows `repository_spec/canonical_case_package_layout_v1.md` and keeps raw legacy `runs/` as mapped retained evidence, not as a wholesale public copy.

## Source-to-Target Mapping Summary

- Root README should be generated from the legacy README, manifest fields, and migration notes.
- Future `manifest.yaml` should be generated from the legacy manifest plus canonical paths and claim-boundary fields.
- `source.sql`, `rewrite_pos_01.sql`, and `rewrite_neg_01.sql` should be copied into `sql/source.sql`, `sql/positives/pos_01.sql`, and `sql/negatives/neg_01.sql`.
- Engine DDL files should be copied into `schema/<engine>/ddl.sql`.
- Witness load files should be copied into `schema/<engine>/load.sql`.
- Checker YAML files should be generated from `validation/check_results.py`, `validation/check_plan_artifacts.py`, retained outputs, and the hard-negative semantics.
- Validation scripts should be treated as legacy validation assets and converted or wrapped for canonical paths and output policy. Spark validation scripts need review because they mention WSL-local execution.
- Public-safe retained JSON/TSV evidence should be promoted into `evidence/retained_controls/`, `evidence/retained_plans/`, and `evidence/hard_negative/`.
- Spark plan text files should not be copied raw; they should become sanitized retained plan copies or stay private/archive-only.

## Hard-Negative, Checker, and Witness Emphasis

The hard-negative target is `sql/negatives/neg_01.sql`. Its expected rejection reason is that it omits the NULL-sensitive suppression required for correlated `NOT IN`; the retained witness makes the negative output differ from source and positive output.

Future checker files should include:

- `checker/checker.yaml`: engine-local witness model with source/positive equality and source/negative divergence.
- `checker/normalization.yaml`: unordered row comparison, tab-separated output, numeric tolerance consistent with the legacy checker.
- `checker/compare_config.yaml`: per-engine source, positive, and negative retained output paths.
- `checker/expected_rejections.yaml`: hard-negative reason and evidence references.

Witness rows are intentionally small:

- `table1`: `(1, 2)`, `(1, 3)`
- `table2`: `(NULL, 1)`, `(2, 1)`

## Runs Retention Strategy

Do not delete or mutate legacy `runs/`.

Future migration should:

- copy public-safe retained result-check JSON and TSV evidence into `evidence/retained_controls/` and `evidence/hard_negative/`;
- copy public-safe PostgreSQL and MySQL JSON plans into `evidence/retained_plans/`;
- sanitize Spark text plan files before public retention because they contain `file:/tmp` traces;
- map every original legacy run artifact in `evidence/runs_retention.yaml` with `do_not_delete_original: true`;
- avoid wholesale public `runs/` publication.

## Manifest Strategy

The future manifest should be generated, not byte-for-byte copied. It should preserve legacy identity fields and add canonical path fields, including SQL, schema, checker, validation, evidence, metadata, notes, and claim boundaries.

It must state:

- `denominator_changed: false`
- `paper_results_changed: false`
- `common_core_membership_changed: false`
- `no_global_leaderboard: true`
- `db_validation_run: false`
- `evidence_regenerated: false`
- `migration_scope: CONS_0005_only`

## Validator v0.3 Implications

After actual migration, `canonical-case` mode should pass only if:

- SQL moves to `sql/`;
- schema/load context is present under `schema/<engine>/`;
- checker YAML exists and parses;
- validation assets are caveated as legacy assets or wrapped;
- retained evidence is mapped and public-safe;
- raw `runs/` is not copied wholesale;
- Spark plans are sanitized or kept out of public retained evidence;
- claim boundaries remain unchanged.

## Public Hygiene Risks

Static precheck found:

- Spark plan text files contain `file:/tmp` traces and need sanitization or private/archive mapping.
- Spark validation scripts contain a WSL-local execution comment and should be cleaned or caveated before canonical publication.
- No prompt/API/token risk was found by the static scan.

## Risks And Abort Conditions

See:

- `CONS_0005_canonical_migration_risk_register.md`
- `CONS_0005_abort_conditions.md`

The highest-risk item is checker semantics: static files show the intended NULL-semantics guard, but human review should approve the expected rejection reason before actual migration.

## Recommended Actual Migration Sequence

1. Confirm release repo is clean and legacy repo is read-only.
2. Re-run the static public hygiene precheck against the legacy case.
3. Create canonical directory structure under `cases/CONS/CONS_0005/`.
4. Copy SQL, schema, witness load, notes, and approved validation assets using canonical names.
5. Generate manifest, checker YAML, data/schema profiles, metadata YAML, and migration notes.
6. Promote public-safe retained JSON/TSV evidence into `evidence/`.
7. Sanitize Spark plan text files or mark them private/archive-only before public retention.
8. Create `evidence/runs_retention.yaml`.
9. Run YAML/JSON/hygiene validation.
10. Run validator v0.3 in `full-case` and `canonical-case` modes.
11. Commit explicit paths only.

## Boundary Statement

This planning task does not migrate `CONS_0005`. It does not start Common-core 40 migration, change denominators, change paper results, change case membership, regenerate evidence, execute DB engines, or modify raw legacy evidence.
