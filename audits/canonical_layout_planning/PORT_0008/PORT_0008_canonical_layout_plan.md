# PORT_0008 Canonical-Layout Full Case Migration Dry-Run Plan

Date: 2026-05-16

## Scope

This is a planning-only dry run for a future `PORT_0008` canonical-layout full case migration. It does not migrate the case, move files, copy legacy files, regenerate evidence, run DB engines, change denominators, change paper results, change case membership, or alter raw legacy evidence.

## Why PORT_0008 After PORT_0004

`PORT_0004` proved that a single-case copy-first pilot can pass validator v0.2 after release-repo hygiene fixes. It was intentionally legacy-compatible and did not test the canonical public-release layout.

`PORT_0008` is the next useful pilot candidate because it exercises the missing dimension: canonical layout plus already validated sanitized Spark plan evidence. It has a completed evidence-mapping pilot with two public-safe sanitized Spark plan files, while the rest of the case package remains in the legacy repo.

## What PORT_0008 Tests That PORT_0004 Did Not

- Canonical `sql/`, `schema/`, `checker/`, `metadata/`, `notes/`, and `evidence/` placement.
- Reuse of existing formal sanitized Spark plan evidence.
- Avoiding wholesale publication of raw `runs/` when some run evidence is not public-safe.
- Generating canonical manifest/checker/metadata from legacy draft files and retained evidence.
- Validator v0.2 full-case behavior on a canonical package rather than a legacy-compatible package.

## Current Legacy Tree Summary

Read-only inspection found 35 files under `cases/PORT/PORT_0008`:

- root docs/metadata: `README.md`, `manifest.yaml`, `promotion_checklist.md`, `risk_notes.md`, `schema_notes.md`, `witness_design_notes.md`;
- SQL: `source.sql`, `rewrite_pos_01.sql`, `rewrite_neg_01.sql`;
- schema: `schema/ddl_pg.sql`, `schema/ddl_mysql.sql`, `schema/ddl_spark.sql`;
- validation and witness loading: six validation/plan scripts plus three witness data SQL files;
- provenance: `provenance/parrot_source_record.json`, `provenance/provenance_notes.txt`;
- retained runs: result/plan summaries, TSV outputs, JSON plans, and two Spark plan text files.

The raw Spark plan text files contain local path traces and must not be copied into public retained evidence as raw files.

## Current Release Evidence-Pilot Tree Summary

The release repo currently has an evidence-only slice:

- `cases/PORT/PORT_0008/MIGRATION_PILOT.md`;
- `cases/PORT/PORT_0008/evidence/runs_retention.yaml`;
- `cases/PORT/PORT_0008/evidence/retained_plans/rewrite_neg_01.sanitized.txt`;
- `cases/PORT/PORT_0008/evidence/retained_plans/rewrite_pos_01.sanitized.txt`.

This slice passes evidence-pilot validation but intentionally fails full-case validation because source SQL, schema, checker, validation, provenance, taxonomy, manifest, and hard-negative SQL are not present in the release case tree.

## Proposed Canonical Target Tree

See `PORT_0008_proposed_canonical_tree.txt` for the concrete target tree. Key points:

- root `manifest.yaml` and `README.md` should be generated for canonical public layout;
- legacy SQL should move by copy into `sql/` paths;
- DDL and witness load SQL should move by copy into `schema/<engine>/` paths;
- checker metadata should be generated because the legacy package has no checker directory;
- current sanitized Spark plans should remain under `evidence/retained_plans/`;
- raw Spark plan text originals should not be copied into public retained evidence;
- raw legacy `runs/` should be reference-only/do-not-delete, not wholesale-copied.

## Source-To-Target Mapping Summary

See `PORT_0008_canonical_file_mapping.csv` for one row per legacy file, existing release pilot artifact, and generated canonical artifact.

Recommended categories:

- copy SQL, DDL, witness load SQL, validation scripts, safe retained JSON/TSV evidence;
- generate canonical manifest, README, checker YAMLs, metadata YAMLs, data profiles, schema profile, migration notes, hard-negative summary, and package validation summary;
- reuse existing sanitized Spark plan files;
- reference raw Spark plan originals only through retention/archive mapping.

## Sanitized Evidence Integration Plan

The future actual migration should reuse the already formalized sanitized public copies:

- `cases/PORT/PORT_0008/evidence/retained_plans/rewrite_neg_01.sanitized.txt`;
- `cases/PORT/PORT_0008/evidence/retained_plans/rewrite_pos_01.sanitized.txt`.

The raw originals remain:

- `cases/PORT/PORT_0008/runs/spark/plans/rewrite_neg_01.txt`;
- `cases/PORT/PORT_0008/runs/spark/plans/rewrite_pos_01.txt`.

Those raw originals must remain do-not-delete in the legacy repo or private/external archive mapping. They must not appear as raw public retained evidence.

## Runs Retention Strategy

Do not copy `runs/` wholesale. Promote public-safe retained outputs and plans into `evidence/`:

- result summary and positive/source TSV outputs into `evidence/retained_controls/`;
- hard-negative output TSVs into `evidence/hard_negative/`;
- JSON plan summaries into `evidence/retained_plans/`;
- sanitized Spark plans into `evidence/retained_plans/`;
- raw Spark plans as private/archive or legacy-reference-only entries in `runs_retention.yaml`.

The future `runs/` directory should be reference-only/empty unless a human explicitly approves a legacy-retained public subtree. New runner outputs must not be written into case-local `runs/` by default.

## Manifest Strategy

Generate a canonical `manifest.yaml`, not a byte-for-byte copy of the legacy manifest. It should preserve legacy identity fields, source family, target engines, draft/admission status, and tags while changing artifact paths to canonical locations.

The manifest must explicitly state:

- denominator changed: false;
- paper results changed: false;
- Common-core membership changed: false;
- no global leaderboard;
- migration scope is `PORT_0008` only;
- engines were not rerun during migration;
- evidence was not regenerated.

See `PORT_0008_manifest_preview.yaml`.

## Validator v0.2 Implications

Current evidence-pilot mode passes. Current full-case advisory mode fails as expected because the release case tree is not a full package.

After actual canonical migration, validator v0.2 should pass if the future task creates:

- manifest;
- source SQL and positive/negative SQL;
- schema directory;
- checker directory or validation checker config;
- validation directory;
- provenance and taxonomy metadata;
- evidence/runs_retention.yaml;
- public-safe retained evidence with no raw local path traces.

See `PORT_0008_validator_expectation_matrix.csv`.

## Risks

Primary risks are raw Spark plan local paths, legacy validation scripts writing to case-local `runs/`, generated checker semantics needing human review, stale draft/admission language in legacy README, and manifest/runs-retention contradiction during path conversion.

See `PORT_0008_canonical_migration_risk_register.md`.

## Abort Conditions

The actual future migration must stop if the release repo is dirty, expected legacy files are missing, hygiene scan fails, copied hashes mismatch, manifest and runs-retention contradict each other, validator v0.2 fails, denominator/paper/membership claims change, raw legacy evidence is mutated, or broad staging such as `git add .` is attempted.

See `PORT_0008_abort_conditions.md`.

## Recommended Actual Migration Sequence

1. Confirm release repo clean and legacy repo read-only state.
2. Re-read this plan, canonical layout spec, retention policy, validator spec, and current evidence-pilot artifacts.
3. Create canonical directories under `cases/PORT/PORT_0008/`.
4. Generate canonical README/manifest/checker/metadata/profile/summary files from legacy sources and this mapping.
5. Copy SQL, schema DDL/load SQL, validation scripts, safe retained controls/plans, notes, and provenance-derived metadata using explicit paths.
6. Reuse existing sanitized Spark plan evidence; do not copy raw Spark plan text into public retained evidence.
7. Generate full canonical `evidence/runs_retention.yaml` with raw originals do-not-delete and private/archive mapping.
8. Run public hygiene scan, YAML/JSON parse checks, SHA256 checks, validator v0.2 full-case, and evidence-pilot regression.
9. Commit explicit paths only.

## Non-Migration Statement

This planning task created only audit/planning outputs and project-control writeback. It did not migrate `PORT_0008`, did not modify `cases/PORT/PORT_0008/`, did not copy or move legacy case files, and did not alter legacy evidence.
