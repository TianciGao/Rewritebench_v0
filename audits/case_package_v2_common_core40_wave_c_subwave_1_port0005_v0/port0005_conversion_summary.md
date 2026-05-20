# PORT_0005 Wave C Subwave 1 Conversion Summary

## Purpose and scope

This bounded writable Wave C subwave converted exactly `PORT_0005` to clean-template-minimal v2. It did not convert any other Wave C case and did not modify already converted pilot, Wave A, or Wave B cases except read-only validator checks.

## Conversion result

- Converted case ID: `PORT_0005`.
- Deferred: no.
- Clean-template-minimal achieved: yes.
- Manifest consistency passed: yes.
- Three-file validation contract passed: yes.
- Schema created/reused: `schemas/parrot_bird_port0005_v0/` created as a per-case external schema package.
- Spark dialect variants retained: yes, `sql/dialect_variants/spark/` remains in the case package.

## Folder-order conversion summary

- Manifest: repaired to semantic v2 contract with explicit non-blocking draft-origin caveat.
- SQL: direct `sql/pos_01.sql` and `sql/neg_01.sql` created from existing nested rewrite SQL; nested compatibility directories removed.
- Schema: external per-case schema package created copy-first; case-local engine schema directories removed; case-local `schema/schema_profile.yaml` retained as profile-only.
- Checker: config-only YAML retained and updated to direct SQL paths and regeneration-first evidence policy.
- Validation: repaired three-file contract adopted with thin shared-runner shim.
- Witness: source-as-oracle witness metadata retained under `witness/`.
- Evidence/metadata/notes/data: removed after live references were represented in manifest, README, checker config, witness, external schema, and regeneration-first policy.

## Protected boundary summary

No `case_sets/`, inventory, reports/results, denominator values, paper results, official metrics, DB/checker execution, global leaderboard, other Wave C cases, or already converted cases were modified. No `evidence/cases/` package was created.

## Exact next safe action

Run `case_package_v2_wave_c_port0005_post_conversion_review_v0` as a read-only parity review for `PORT_0005`, then proceed to the next precleared Wave C subwave only if the review passes.
