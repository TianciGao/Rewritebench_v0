# case_package_v2_metadata_notes_runs_layers_pilot_v0

## Purpose and Scope

This branch-only writable pilot handled only the metadata, notes, and runs-classification layers for five v2 pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Previous writable pilots already converted manifest, SQL, schema, checker, validation, witness, and evidence-reference layers. This task did not perform README/validator closeout, DB/checker execution, official metric computation, report/result migration, denominator updates, case-set updates, paper-result changes, evidence deletion, non-empty runs deletion, or leaderboard creation.

## Converted/Classified Layers

- Metadata: case-local `metadata/` files were classified and mapped under `compatibility.metadata_legacy` in each manifest. No metadata files were deleted.
- Notes: public-safe human-readable notes were copy-first copied into `evidence/cases/<POOL>/<CASE_ID>/notes/` and mapped under `compatibility.notes_legacy`. Original case-local notes were not deleted.
- Runs: case-local `runs/` directories were classified. Each pilot case has only a tracked placeholder `runs/README.md`; no runs deletion was performed.

## Metadata Classification Summary

Each pilot case has the expected metadata files:

- `metadata/provenance.yaml`
- `metadata/taxonomy.yaml`
- `metadata/denominator_eligibility.yaml`
- `metadata/artifact_paths.yaml`
- `metadata/engine_support.yaml`

The files were stable, public-safe, and already reflected in manifest canonical fields or compatibility context. They remain case-local compatibility assets pending later cleanup approval.

## Notes Externalization Summary

Each pilot case had five human-readable notes:

- `notes/migration_notes.md`
- `notes/promotion_checklist.md`
- `notes/risk_notes.md`
- `notes/schema_notes.md`
- `notes/witness_design_notes.md`

These notes were copied to the corresponding external evidence notes directory. The source notes remain in place. The hygiene scan found no credentials, private local paths, API keys, prompts, model traces, or raw debug traces selected for copy.

## Runs Classification Summary

All five case-local `runs/` directories were classified as `placeholder_only` with one tracked `runs/README.md`. No retained evidence files were found under case-local `runs/` in these pilot cases. Future cleanup action is `remove_empty_runs_after_approval`.

## Deletions

No files or directories were deleted. In particular:

- Metadata files deleted: no.
- Original case-local notes deleted: no.
- Case-local evidence deleted: no.
- Runs deleted: no.
- Non-empty runs deleted: no.

## Protected Boundary Summary

- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.
- README/validator conversion: no.
- Legacy repo modified: no.

## Validation Summary

Static v2 validation passed for all five pilot cases. Unit tests under `tests/case_package_v2` passed. Summary JSON boundary assertions passed. `git diff --check` passed.

## Exact Next Safe Action

Authorize `case_package_v2_readme_validator_closeout_pilot_v0` to update only README wording and validator expectations for the same five pilot cases, branch-only, after confirming no protected benchmark-surface changes and no DB/checker execution.
