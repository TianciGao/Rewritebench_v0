FUTURE PROMPT — DO NOT EXECUTE NOW

Task: CONS canonical-layout migration batch after maintainer approval.

Hard boundaries:
- Do not modify `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`.
- Do not run DB engines, validation scripts, LLM calls, timing workloads, or evidence regeneration.
- Do not change Common-core membership, denominator, paper results, case admission status, case_sets, or reports/evaluation/common_core_v0.
- Do not use `git add .`.
- Abort on dirty release repo, missing legacy files, unapproved expected-rejection wording, public hygiene failure, copied hash mismatch, validator failure, raw legacy evidence mutation, or denominator/paper-result/case-membership change.

Required behavior:
- Use canonical layout v1 and the CONS_0005 canonical pilot pattern.
- Create each selected case under `cases/CONS/<CASE_ID>/` only.
- Copy source/positive/negative SQL, schema, witness data, and retained validation assets from legacy read-only.
- Generate `checker/expected_rejections.yaml` using maintainer-approved wording from `audits/cons_hard_negative_approval/cons_expected_rejections_preview.yaml`.
- Preserve validation scripts only as retained legacy validation assets; add the output-policy caveat.
- Promote only public-safe evidence; sanitize Spark plan text with local paths before public packaging or map raw files archive-only.
- Create `evidence/runs_retention.yaml` with raw legacy do-not-delete mappings.
- Run validator v0.3 full-case and canonical-case for the migrated cases and regression validators for existing pilots/batches.
- Update `project_control/MIGRATION_STATUS.md` and append `project_control/MIGRATION_RUN_LOG.md`.
- Commit explicit paths only and push to origin main.

Selected cases:
- CONS_0012
- CONS_0024
- CONS_0036
- CONS_0037

Expected rejection sources:
- CONS_0012: use the corresponding preview entry and maintainer-approved wording before migration.
- CONS_0024: use the corresponding preview entry and maintainer-approved wording before migration.
- CONS_0036: use the corresponding preview entry and maintainer-approved wording before migration.
- CONS_0037: use the corresponding preview entry and maintainer-approved wording before migration.

Validation commands must include:
- `python scripts/dev/validate_case_package.py --mode full-case` for selected cases.
- `python scripts/dev/validate_case_package.py --mode canonical-case` for selected cases.
- Evidence-pilot and full-case/canonical-case regressions over existing migrated pilots and batches.
- `python -m py_compile scripts/dev/validate_case_package.py`.
- `git diff --check` and `git status -sb`.

Final response must report legacy modified no, release files created/modified, per-case hard-negative reason, public hygiene/sanitization result, validator result, commit hash, push result, and exact next safe action.
