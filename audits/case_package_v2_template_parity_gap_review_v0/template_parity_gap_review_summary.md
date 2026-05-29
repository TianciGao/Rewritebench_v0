# case_package_v2_template_parity_gap_review_v0

## Purpose and Scope

This branch-only audit compares the five converted case-package v2 pilot cases against the clean v2 case-local template proposed for public-facing packages.

Pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

This is a read-only parity/gap review. It did not modify case packages, schemas, evidence, runs, case sets, inventory, reports, results, denominators, paper results, or leaderboard outputs. It did not run DB/checker execution or compute official metrics.

## Clean v2 Template Definition

Clean required case-local assets:

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
```

Optional witness assets:

```text
witness/witness_profile.yaml
witness/data_profile.yaml
witness/correct_result.csv
```

Not clean-template-required case-local assets:

```text
data/
schema/<engine>/ddl.sql
schema/<engine>/load.sql
evidence/
metadata/
notes/
runs/
sql/positives/
sql/negatives/
validation/run_<engine>_*.sh
per-case checker Python/scripts
__pycache__/
```

External v2 assets:

```text
schemas/<SCHEMA_ID>/
evidence/cases/<POOL>/<CASE_ID>/
runs/user/<run_id>/
results/retained/
reports/
```

## High-level Parity Result

All five pilot cases have every clean-template-required asset present and pass the static v2 validator. None are fully clean-template-minimal yet because each still retains temporary v1/v1-compatible directories or files.

Clean-template parity status: `passes_v2_static_validation_with_compatibility_gaps`.

## Per-case Gap Summary

- `PERF_0006`: required assets present; optional `witness_profile.yaml`, `data_profile.yaml`, and `correct_result.csv` present; remaining gaps are compatibility SQL dirs, case-local executable schema copies, case-local evidence, metadata, notes, placeholder runs, data, and old engine-specific validation scripts.
- `PERF_0007`: required assets present; optional `witness_profile.yaml` present; `data_profile.yaml` and `correct_result.csv` absent under `witness/` by policy; same compatibility gaps as `PERF_0006`.
- `CONS_0005`: required assets present; optional `witness_profile.yaml` present; witness static files absent by policy; data fixture compatibility remains.
- `PORT_0003`: required assets present; optional `witness_profile.yaml` present; witness static files absent by policy; additional `sql/dialect_variants/spark/` remains as portability-specific manual-review compatibility.
- `LONGTAIL_0011`: required assets present; optional `witness_profile.yaml` present; witness static files absent by policy; data fixture compatibility remains.

## Intentional v2 Differences From Colleague Template

The pilot keeps `schema/schema_profile.yaml` case-local by policy. Executable DDL/load are external under `schemas/<SCHEMA_ID>/`. This profile-only schema directory is an intentional v2 refinement, not a gap.

The pilot also supports optional `witness/` metadata and source-as-oracle execution. Missing static `correct_result.csv` is not a gap when the manifest records source-as-oracle policy.

## Temporary Compatibility Layers

Temporary compatibility layers present across the five cases:

- nested `sql/positives/` and `sql/negatives/`
- case-local `schema/<engine>/ddl.sql` and `load.sql`
- case-local `evidence/`
- case-local `metadata/`
- case-local `notes/`
- case-local `runs/README.md`
- old engine-specific validation scripts
- case-local `data/`

`PORT_0003` additionally retains Spark dialect-variant SQL under `sql/dialect_variants/spark/`.

## Deletion and Cleanup Readiness

No deletion is authorized by this audit. Future cleanup can be split:

- Low-risk after approval: nested SQL compatibility paths, copied case-local notes, placeholder-only `runs/README.md`.
- Medium-risk/manual review: case-local `data/`, metadata files, old engine-specific validation scripts, case-local schema engine files.
- Retention-mapping required: case-local `evidence/` and any retained evidence references.
- Manual-review required: `PORT_0003` dialect variants before any clean-template pruning.

## Witness Static-file Policy

All five manifests record `witness.mode: source_as_oracle`. `witness/witness_profile.yaml` exists for all five cases. `PERF_0006` also retains optional static `witness/data_profile.yaml` and `witness/correct_result.csv`. The other four cases do not have static witness files under `witness/`, which is allowed because static witness files are optional and must never be fabricated.

## Evidence and Runs Retention Constraints

External evidence packets exist under `evidence/cases/<POOL>/<CASE_ID>/` for all five cases. Case-local `evidence/` remains retained compatibility material and must not be deleted without retention mapping and explicit approval. Case-local `runs/` contains only `runs/README.md` placeholders for all five cases, but cleanup still requires approval because case-local runs are governed by retained-evidence policy.

## Exact Next Safe Action

Authorize `case_package_v2_clean_template_cleanup_pilot_v0` only for cleanup actions marked ready in this audit, with explicit path staging, no retained-evidence deletion without mapping, and no changes to protected benchmark surfaces.
