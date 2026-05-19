# Case Package v2 Conversion Rulebook Summary

## Purpose and Scope

This branch-only task records the conversion rules for moving current v1 and v1-compatible case packages toward the v2 template on `feature/case-package-v2-external-schema`.

It is documentation and planning only. It does not convert cases, modify schemas, run DB/checker execution, compute metrics, render paper tables, update reports/results, change denominators, change case-set membership, delete evidence, delete case-local runs, or create leaderboard output.

## Why This Rulebook Is Needed

The `PERF_0006` v2 pilot established a concrete external-schema pattern and later normalized its manifest. Future conversion tasks need a stable rulebook so they do not make ad hoc decisions about SQL layout, schema externalization, evidence externalization, validation wrappers, witness files, compatibility directories, or cleanup timing.

## Final v2 Template Target

Clean v2 case-local packages should contain:

```text
README.md
manifest.yaml
sql/source.sql
sql/pos_01.sql
sql/neg_01.sql
checker/checker.yaml
checker/normalization.yaml
checker/compare_config.yaml
checker/expected_rejections.yaml
validation/run_validation.sh
validation/run_plan_collection.sh
```

Optional compatibility-only directories are `runs/` and `witness/`. Case-local `schema/`, `data/`, `evidence/`, `metadata/`, `notes/`, nested SQL directories, and engine-specific validation scripts are not required in the final clean v2 shape.

## How Extra Information Is Placed

- Schema assets are copy-first externalized to `schemas/<SCHEMA_ID>/`.
- Evidence assets are copy-first externalized to `evidence/cases/<POOL>/<CASE_ID>/`.
- Provenance, denominator eligibility, taxonomy, artifact-path, source-family, legacy SQL, case-local schema, and validation compatibility metadata are merged into `manifest.yaml`.
- User-run outputs remain under `runs/user/<run_id>/`.
- Paper retained outputs remain under `results/retained/` and `reports/` only after separate authorization.

## Validation Script Consolidation Policy

Every v2 package converges to two thin public wrappers:

- `validation/run_validation.sh`
- `validation/run_plan_collection.sh`

Wrappers must accept `--engine postgres|mysql|spark` and `--target source|positive|negative|all`, resolve manifest references, call shared logic under `scripts/` or `src/`, and write only to explicit local output roots. They must not write new output to case-local `runs/`, store credentials, compute official metrics, create paper results, or create leaderboard output.

Old engine-specific validation and plan scripts are compatibility assets. Delete them only after wrappers pass validation and unique logic has been moved to shared code or archived as public-safe notes.

## Data, Witness, and Source-as-oracle Policy

`data_profile.yaml` and `correct_result.csv` are optional, generated, or external. They are not required case-local v2 content. Runtime user-run checking defaults to source-as-oracle: execute source SQL and candidate SQL in the same local schema context and compare normalized results.

## Evidence and Runs Cleanup Policy

Empty or placeholder-only case-local `runs/` may be deleted after audit. Non-empty retained evidence must be retention-mapped or copy-first externalized before deletion. Case-local `evidence/` follows the same rule. Sensitive raw logs, prompt/token/API/model traces, private paths, credentials, stdout/stderr/debug dumps, and local-only traces must not be copied into public evidence.

## Batch Conversion Algorithm

The future converter should run in phases:

- Phase A: read-only inventory and file disposition plan.
- Phase B: non-destructive conversion with direct SQL, schema_ref, evidence_ref, validation wrappers, and copy-first externalization.
- Phase C: static validation and protected-path checks.
- Phase D: cleanup only for audited empty, placeholder, or duplicated compatibility assets.
- Phase E: explicit staging and batch commit.

## Stop Conditions

Stop on missing source SQL, missing required positive SQL, missing checker config, unresolved schema_ref, uncertain evidence classification, non-empty runs without mapping, sensitive trace detection, validator failure, protected path changes, denominator or paper-result changes, or leaderboard output.

## Exact Next Safe Action

Authorize `case_package_v2_batch_converter_plan_v0` to produce a read-only converter dry-run over `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`, without converting all files yet.
