# PERF_0006 v2 Format Normalization Summary

## Purpose and Scope

This branch-only task normalized the internal v2 manifest/reference shape for the existing `PERF_0006` case-package v2 pilot on `feature/case-package-v2-external-schema`.

The task did not convert additional cases, delete compatibility directories, run DB/checker execution, compute metrics, update reports/results, change denominators, change paper results, or create leaderboard output.

## Files Modified

- `cases/PERF/PERF_0006/manifest.yaml`
- `cases/PERF/PERF_0006/README.md`
- `src/sql_rewrite_bench/case_package_v2_resolver.py`
- `tests/case_package_v2/test_case_package_v2_resolver.py`

The resolver/test changes were limited to a validator false-positive alignment: the required top-level `compatibility` block is now recognized as a compatibility key, and the read-only `PERF_0006` test no longer expects pre-normalization findings.

## Canonical Fields Normalized

- `sql.positives` and `sql.negatives` now use direct v2 string paths.
- `schema_ref` now uses `schema_ref.engines.<engine>.ddl/load`.
- `checker` now uses `checker.config`, `checker.normalization`, `checker.compare_config`, and `checker.expected_rejections`.
- `witness` now records `mode: source_as_oracle`, `data_profile_status: external_or_generated`, and `correct_result_status: materialized`.
- `evidence_ref` now records pending copy-first externalization and resolves required case-local compatibility evidence through repository-relative paths.
- `validation` now contains only canonical wrapper entrypoints.
- Legacy SQL, case-local schema, and engine-specific validation references now live under a top-level `compatibility` block.

## Compatibility Fields Retained

- Old `sql/positives/` and `sql/negatives/` directories were retained.
- Case-local `schema/` was retained as a v1 compatibility copy.
- Case-local `evidence/` was retained pending copy-first external evidence adoption.
- Case-local `runs/` was retained as legacy retained evidence only.
- Engine-specific validation scripts were retained under `compatibility.validation_legacy`.

## Warnings Resolved

The v2 validator now reports `overall_status=pass` and `format_findings=0` for `PERF_0006`.

Resolved warning classes include mapping-shaped SQL entries, top-level engine-shaped `schema_ref`, compatibility `checker.checker`, missing witness policy fields, missing `evidence_ref`, and engine-specific validation entries in the canonical validation block.

## Warnings Intentionally Retained

No validator format findings remain. Compatibility assets are intentionally retained as non-finding policy state because deletion requires separate authorization and retention mapping.

## No-deletion Summary

No case-local schema, evidence, runs, data, metadata, notes, or validation compatibility assets were deleted.

## Validation Summary

- Manifest canonical-shape assertion: passed.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PERF/PERF_0006`: passed.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed.
- `git diff --check`: passed.
- Protected benchmark surfaces were not changed.

## Exact Next Safe Action

Authorize a branch-only multi-pool v2 pilot using the normalized `PERF_0006` manifest as the canonical example, limited to `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`, with no merge to `main` until pilot review is accepted.
