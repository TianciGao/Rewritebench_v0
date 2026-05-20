# Common-core 40 v2 Final Closeout Audit

## Purpose and Scope

This read-only closeout reviewed all 40 Common-core v0 cases on branch `feature/case-package-v2-external-schema` after the pilot, Wave A, Wave B, Wave C PORT conversions, manifest semantic contract repair, validation three-file contract repair, evidence policy migration, and clean-template cleanup work. It did not modify case packages, schemas, case sets, inventory, reports, results, denominators, paper results, or execution outputs.

## Common-core 40 Reviewed

- PERF: 16 cases
- CONS: 9 cases
- PORT: 9 cases
- LONGTAIL: 6 cases
- Total: 40 cases

## Conversion Wave Summary

- Accepted pilot cases remain validator-clean, but five pilot packages still retain empty compatibility directories that block final clean-template-minimal closeout.
- Wave A, Wave B, PORT_0005, Wave C subwave 2, and final dialect PORT conversions remain validator-clean and clean-template-minimal under the final v2 policy.
- Special PORT dialect variants are retained as semantic optional v2 assets rather than dirty compatibility paths.

## Validator Summary

- Static v2 validators passed: 40/40.
- Unit tests passed: 19/19.
- No DB/checker execution, official metrics, report rendering, or leaderboard creation was performed.

## Clean-template-minimal Summary

- Clean-template-minimal packages passed: 35/40.
- Remaining structural blockers: 15 forbidden path entries across 5 pilot cases.
- Blocked cases: PERF_0006, PERF_0007, CONS_0005, PORT_0003, LONGTAIL_0011.
- The remaining blockers are `notes/`, `sql/positives/`, and `sql/negatives/` under each blocked pilot case. They appear empty, but this task is read-only and does not delete them.

## Manifest Semantic Contract Summary

- Manifest semantic contract passed: 40/40.
- All manifests use object-form SQL metadata, schema profile/external profile fields, checker config paths, source-as-oracle witness policy, regeneration-first `evidence_policy`, and no mandatory `evidence_ref`.

## Dialect Variant Retention Summary

- Retained dialect-variant cases: PORT_0003, PORT_0004, PORT_0005, PORT_0013.
- `PORT_0003`, `PORT_0004`, `PORT_0005`, and `PORT_0013` retain `sql/dialect_variants/` as semantic PORT assets.
- Dialect variants are not blockers and were not deleted.

## Validation Three-file Contract Summary

- Validation three-file contract passed: 40/40.
- Each package has `validation/run_validation.sh`, `validation/run_plan_collection.sh`, and a thin `validation/run_engine_queries.py` shim.
- Wrappers do not call old engine-specific scripts, write case-local `runs/`, or require case-local schema engine dirs.

## Evidence Policy Summary

- All reviewed manifests use regeneration-first `evidence_policy` with `static_case_evidence: not_required`.
- Static `evidence/cases/` is not required for clean v2 and was not created by this audit.

## Schema Policy Summary

- All 40 cases resolve `schema.external_profile` under `schemas/<SCHEMA_ID>/schema_profile.yaml`.
- Case-local schema engine directories are absent in all 40 reviewed packages.

## PERF_0077 / PERF_0082 Source-path Caveat Note

`PERF_0077` and `PERF_0082` retain explicit `source_path_not_recovered` caveats. These do not block case-package v2 validator pass or case-package closeout, but they do block final public source-path closeout and require a separate narrow provenance follow-up.

## Protected Boundary Summary

- Case package files modified by this audit: no.
- Schemas modified by this audit: no.
- `case_sets/`, inventory, reports/results, denominators, paper results: unchanged.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.
- Dialect variants deleted: no.

## Exact Next Safe Action

Run a narrow writable cleanup for leftover empty pilot compatibility directories (`notes/`, `sql/positives/`, and `sql/negatives/`) in `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`; rerun this final closeout; then perform the `PERF_0077`/`PERF_0082` source-path provenance follow-up before public release closeout.
