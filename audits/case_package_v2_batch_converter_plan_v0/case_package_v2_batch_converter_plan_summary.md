# Case Package v2 Batch Converter Plan Summary

## Purpose and Scope

This task produced a read-only v2 batch conversion plan for exactly five pilot cases on `feature/case-package-v2-external-schema`:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

No case files, schema files, evidence files, case sets, inventory, reports, results, denominator files, or paper-result files were modified. No DB/checker execution, metric computation, paper rendering, cleanup, evidence deletion, runs deletion, or leaderboard output occurred.

## Read-only Dry-run Statement

The dry-run inventoried the current case packages and classified proposed v2 disposition using the conversion rulebook. It wrote only audit outputs and project-control updates.

## Per-case Readiness Summary

- `PERF_0006`: already normalized to canonical v2 manifest shape; schema external package exists; evidence externalization and compatibility cleanup remain pending.
- `PERF_0007`: source/checker/schema/evidence assets are present; direct SQL copies, canonical manifest shape, wrappers, external schema, and external evidence are still needed. Automatic full conversion is not safe until schema reuse and validation script logic are reviewed.
- `CONS_0005`: source/checker/schema/evidence assets are present; conversion is structurally straightforward but still needs wrappers, schema externalization, and validation script review.
- `PORT_0003`: assets are present but dialect variants and portability-specific Spark/MySQL logic require manual review before automatic conversion.
- `LONGTAIL_0011`: assets are present but structural/tie-sensitive semantics and rich engine-specific validation scripts require manual review before automatic conversion.

## Common Conversion Patterns

- Four non-normalized cases still use `sql/positives/pos_01.sql` and `sql/negatives/neg_01.sql`.
- Four non-normalized cases still use top-level `schema`, `checker.checker`, `validation` engine-specific entries, and `evidence` blocks.
- All five cases have case-local `runs/` containing only a policy README; cleanup is still separate and not performed here.
- All five cases have case-local retained evidence that should be copy-first externalized before any deletion.

## Major Blockers

- External schema packages exist only for `PERF_0006`.
- `PERF_0007` schema/load differs from the current `tpch_common_core_v0` pilot schema and should not be silently reused.
- `PORT_0003` has Spark dialect variant SQL and portability-specific validation logic.
- `LONGTAIL_0011` has tie-sensitive structural semantics and substantial engine-specific validation logic.
- Engine-specific validation scripts write to case-local `runs/` and must be consolidated before cleanup.

## Automatic Conversion Candidates

No new case is fully automatic-safe for writable conversion. `PERF_0006` is already normalized. For the other four, direct SQL copy creation and manifest draft generation can be automated only after the read-only plan is accepted, but schema/evidence/wrapper review remains required.

## Manual-review Candidates

- `PERF_0007`: schema reuse versus new external schema id; validation scripts write case-local runs.
- `CONS_0005`: validation script consolidation and external schema naming.
- `PORT_0003`: dialect variants and target-specific validation logic.
- `LONGTAIL_0011`: structural/tie-sensitive semantics and validation logic.

## Schema Externalization Plan

- Keep `tpch_common_core_v0` for `PERF_0006`.
- Propose a separate `tpch_perf0007_v0` schema for `PERF_0007` because the local DDL/load differs from `PERF_0006`.
- Propose `calcite_core_sql_tests_cons0005_v0` for `CONS_0005`.
- Propose `parrot_bird_port0003_v0` for `PORT_0003`.
- Propose `sqlstorm_stackoverflow_longtail0011_v0` for `LONGTAIL_0011`.

All non-`PERF_0006` schemas require copy-first externalization.

## Evidence and Runs Externalization Plan

Case-local `evidence/` should be copy-first externalized into `evidence/cases/<POOL>/<CASE_ID>/`. Case-local `runs/` directories are placeholder-policy directories only, but deletion remains a separate cleanup action after audit.

## Validation Consolidation Plan

`PERF_0006` already has generic wrappers. The other four cases need `validation/run_validation.sh` and `validation/run_plan_collection.sh`. Existing engine-specific scripts contain unique engine logic and write to case-local `runs/`; they should be retained as compatibility assets until shared wrapper logic is implemented.

## Manifest Conversion Plan

All non-normalized cases need canonical direct SQL lists, `schema_ref.engines`, `checker.config`, source-as-oracle witness policy, `evidence_ref`, canonical validation wrapper refs, and a top-level `compatibility` block for legacy paths and scripts.

## Exact Next Safe Action

Authorize `case_package_v2_batch_conversion_pilot_v0` only for a non-destructive writable pilot that first handles direct SQL copies, manifest draft normalization, wrapper creation, and copy-first external schema/evidence plans for cases whose manual-review blockers are resolved.
