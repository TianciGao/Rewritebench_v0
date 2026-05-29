# Future Prompt: case_package_v2_common_core40_wave_c_execution_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not inspect or modify the legacy repo.

Task type:
This is a bounded writable Wave C conversion execution task only after explicit maintainer preclearance.

Allowed target cases:
Convert only Wave C cases explicitly marked readiness-approved by `case_package_v2_common_core40_wave_c_preclearance_v0` or an equivalent maintainer decision packet. Defer every case that still requires D008, dialect, schema, provenance, taxonomy, or public-safety manual review.

Hard boundaries:
- Do not invent provenance, taxonomy, source identity, source paths, benchmark identity, draft origin, or dialect semantics.
- Preserve `sql/dialect_variants/` when semantically needed; never delete dialect variants as generic cleanup.
- Do not modify `case_sets/`, inventory, reports/results, denominator values, paper results, official metrics, DB/checker execution, or leaderboard output.
- Do not create top-level `evidence/cases/` for clean v2.

Required conversion shape:
- `manifest.yaml` with colleague-style semantic v2 contract.
- `sql/source.sql`, `sql/pos_01.sql`, `sql/neg_01.sql`, optional `sql/dialect_variants/` only when approved.
- `schema/schema_profile.yaml` plus verified external `schemas/<SCHEMA_ID>/schema_profile.yaml` and DDL/load files.
- Config-only checker YAML files.
- Thin `validation/run_validation.sh` and `validation/run_plan_collection.sh` wrappers that do not call legacy engine scripts or write case-local runs.
- Source-as-oracle witness policy.
- Regeneration-first `evidence_policy` and no mandatory `evidence_ref`.

Validation:
Run static v2 validator for every converted case and regression validators for the 32 already converted cases. Run `tests/case_package_v2`. Run JSON, CSV, protected-boundary, and `git diff --check` checks. No DB/checker execution.
