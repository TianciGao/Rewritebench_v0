# Case Package v2 Runner / Validator Compatibility v0

## Purpose and Scope

This branch-only task adds non-destructive v2 reference validation for case packages on:

`feature/case-package-v2-external-schema`

It creates a static resolver and developer validator for `schema_ref`, optional `evidence_ref`, direct SQL paths, checker references, witness policy fields, and validation entrypoints.

This task does not modify case packages, convert additional cases, modify schema assets, run DB engines, run checkers, collect timing, compute official metrics, update reports/results, update retained evidence, change denominators, change paper results, delete case-local `runs/`, or create leaderboard output.

## Files Created

- `src/sql_rewrite_bench/case_package_v2_resolver.py`
- `scripts/dev/validate_case_package_v2_refs.py`
- `tests/case_package_v2/test_case_package_v2_resolver.py`
- `audits/case_package_v2_runner_validator_compatibility_v0/`

## Resolver Behavior

The resolver reads `manifest.yaml` and resolves:

- `sql.source`
- `sql.positives`
- `sql.negatives`
- `checker.config`
- `checker.normalization`
- `checker.compare_config`
- `checker.expected_rejections`
- `schema_ref.engines.<engine>.ddl`
- `schema_ref.engines.<engine>.load`
- optional `evidence_ref` paths
- witness metadata paths when present
- validation entrypoints

The resolver supports canonical v2 shapes and explicit compatibility fallbacks for the existing `PERF_0006` pilot. Compatibility fallbacks are reported as warnings, not rewritten.

## Validator Behavior

The developer validator is:

```bash
PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PERF/PERF_0006
```

It checks path existence, path safety, and internal manifest-format consistency only. It does not execute SQL, run DB engines, invoke checkers, parse retained evidence, compute metrics, or write into the case package.

## PERF_0006 Recheck Result

`PERF_0006` was rechecked in read-only mode.

Result:

- overall status: pass
- resolved references: 17
- internal checks: 40
- format findings: 19 warning-only findings

All required referenced paths resolved safely and existed. Findings are compatibility warnings for branch-pilot shape differences, including:

- SQL positive/negative entries are mapping objects rather than direct string entries.
- `checker.checker` is used as a compatibility source for canonical `checker.config`.
- `schema_ref` uses top-level engine keys rather than canonical `schema_ref.engines`.
- `evidence_ref` is not yet present.
- witness policy fields are not fully canonical.
- engine-specific validation entries remain as compatibility assets.

No case file was modified to fix these findings.

## Internal Format Guard

The validator records an internal-format contract and emits per-field checks. It fails on unsafe paths and missing required v2 paths. It warns, without rewriting, for compatibility assets that are expected during branch adoption.

## Directory Classification

`PERF_0006` directories were classified without modification:

- `checker/`: keep as v2 case-local checker policy.
- `data/`: compatibility metadata.
- `evidence/`: compatibility copy pending `evidence_ref`.
- `metadata/`: governance metadata.
- `notes/`: optional stable notes.
- `runs/`: legacy retained evidence only.
- `schema/`: compatibility copy pending `schema_ref` compatibility.
- `sql/`: required v2 direct SQL assets.
- `validation/`: wrapper entrypoints plus compatibility scripts.
- `witness/`: optional lightweight witness metadata/static result.

## Validation Summary

Validation passed:

- unit tests passed
- `PERF_0006` read-only validator command passed
- summary JSON parsed
- no files under `cases/` changed
- no files under `schemas/` changed
- no files under `case_sets/` changed
- no inventory changes
- no reports/results changes
- no denominator changes
- no paper-result changes
- no DB/checker execution outputs
- no leaderboard output
- `git diff --check` passed

## Compatibility Gaps

Remaining gaps are documented in `v2_compatibility_gaps.csv`. The next task should decide whether to update `PERF_0006` manifest shape to the canonical internal format or keep current compatibility forms until the multi-pool pilot.

## Exact Next Safe Action

Authorize a branch-only `case_package_v2_multi_pool_pilot_v0` that uses the new validator, optionally first normalizes `PERF_0006` manifest internal shape to canonical v2, and then pilot-converts only `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011` without modifying `main`.
