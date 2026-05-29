# Wave C Final Dialect PORT Conversion Summary

## Purpose and scope

This bounded writable task converted exactly the final dialect-variant Wave C PORT cases: `PORT_0004` and `PORT_0013`.

The task did not modify `PORT_0005`, subwave 2 PORT cases, pilot cases, Wave A cases, Wave B cases, `case_sets/`, inventory, reports/results, denominator values, paper results, official metrics, DB/checker execution, `evidence/cases/`, or leaderboard outputs.

## Conversion result

- Target case IDs: `PORT_0004`, `PORT_0013`.
- Converted case IDs: `PORT_0004`, `PORT_0013`.
- Deferred case IDs: none.
- Clean-template-minimal cases: 2.
- Dialect variants retained: yes, Spark dialect variants remain under `sql/dialect_variants/spark/` for both cases.
- Manifest consistency passed: yes.
- Three-file validation contract passed: yes.
- Schemas created/reused: `parrot_bird_port0004_v0` and `parrot_bird_port0013_v0` created as per-case external schema packages.

## Folder-order conversion summary

- Manifest: converted to the repaired semantic v2 contract using recovered/precleared provenance and explicit caveats where required.
- SQL: direct `sql/pos_01.sql` and `sql/neg_01.sql` paths were created from existing nested rewrite SQL before nested compatibility directories were removed.
- Dialect variants: existing Spark dialect variant SQL files were retained and recorded as optional semantic PORT assets.
- Schema: per-case external schema packages were created copy-first from case-local DDL/load assets; case-local engine schema directories were removed after verification.
- Checker: config-only YAML retained and rewritten to direct SQL paths with regeneration-first evidence policy.
- Validation: repaired three-file contract adopted with thin shared-runner shims.
- Witness: source-as-oracle witness metadata retained under `witness/`.
- Evidence/metadata/notes/data: removed after stable semantic content was represented in manifest, README, checker config, witness policy, external schema, and regeneration-first evidence policy.

## Protected boundary summary

Only `PORT_0004`, `PORT_0013`, their two external schema packages, this audit directory, and project-control files were modified. No other PORT, pilot, Wave A, Wave B, `case_sets/`, inventory, reports/results, denominator, paper-result, official-metric, DB/checker execution, `evidence/cases/`, or leaderboard changes were made.

## Exact next safe action

Run a read-only Common-core 40 v2 final closeout covering all converted Common-core v2 cases, with particular checks for retained dialect variants in `PORT_0003`, `PORT_0004`, `PORT_0005`, and `PORT_0013`.
