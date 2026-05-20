# Common-core 40 v2 Final Closeout Rerun

## Purpose and Scope

This branch-only read-only rerun reviewed all 40 Common-core v0 v2 case packages after the pilot leftover compatibility directory cleanup. It did not modify case packages, schemas, `case_sets/`, inventory, reports/results, denominators, paper results, official metrics, DB/checker execution, evidence surfaces, or leaderboard outputs.

## Why This Is a Rerun

The previous final closeout passed static validators for 40/40 cases but found 15 clean-template-minimal blockers: empty `notes/`, `sql/positives/`, and `sql/negatives/` directories under the five early pilot cases. The cleanup task removed exactly those 15 empty directories and recorded 0 skips.

## Common-core 40 Reviewed

- PERF: 16 cases
- CONS: 9 cases
- PORT: 9 cases
- LONGTAIL: 6 cases
- Total: 40 cases

## Validator Summary

- Static v2 validators passed: 40/40.
- Unit tests passed: 19/19.
- No DB/checker execution, official metrics, report rendering, or leaderboard creation was performed.

## Clean-template-minimal Summary

- Clean-template-minimal packages passed: 40/40.
- Remaining blockers: 0.
- The five pilot cases no longer contain `notes/`, `sql/positives/`, or `sql/negatives/`.

## Manifest Semantic Contract Summary

- Manifest semantic contract passed: 40/40.
- All manifests use object-form SQL metadata, schema profile/external profile fields, checker config paths, source-as-oracle witness policy, regeneration-first `evidence_policy`, and no mandatory `evidence_ref`.

## Validation Three-file Contract Summary

- Validation three-file contract passed: 40/40.
- Each package has `validation/run_validation.sh`, `validation/run_plan_collection.sh`, and a thin `validation/run_engine_queries.py` shim.
- Wrappers do not call old engine-specific scripts, write case-local `runs/`, or require case-local schema engine dirs.

## Dialect Variant Retention Summary

- Retained dialect-variant cases: PORT_0003, PORT_0004, PORT_0005, PORT_0013.
- `PORT_0003`, `PORT_0004`, `PORT_0005`, and `PORT_0013` retain `sql/dialect_variants/` as semantic optional PORT assets.
- Dialect variants are not blockers and were not deleted.

## Evidence Policy Summary

- All reviewed manifests use regeneration-first `evidence_policy` with `static_case_evidence: not_required`.
- Static `evidence/cases/` is not required for clean v2 and was not created by this audit.

## Schema Policy Summary

- All 40 cases resolve `schema.external_profile` under `schemas/<SCHEMA_ID>/schema_profile.yaml`.
- Case-local schema engine directories are absent in all 40 reviewed packages.

## Remaining Blocker Summary

- Case-package closeout blockers: 0.
- Final public source-path closeout blockers: `PERF_0077` and `PERF_0082` source-path provenance caveats remain unresolved.

## PERF_0077 / PERF_0082 Source-path Caveat Note

`PERF_0077` and `PERF_0082` retain explicit `source_path_not_recovered` caveats. These do not block Common-core 40 v2 case-package closeout, but they do block final public source-path closeout and require a separate narrow provenance follow-up.

## Protected Boundary Summary

- Case package files modified by this rerun: no.
- Schemas modified by this rerun: no.
- `case_sets/`, inventory, reports/results, denominators, paper results: unchanged.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.
- `evidence/cases/` created: no.
- Dialect variants deleted: no.

## Exact Next Safe Action

Run a narrow `PERF_0077`/`PERF_0082` source-path provenance follow-up. After it resolves or explicitly closes those source-path caveats, proceed to final public-release closeout planning.
