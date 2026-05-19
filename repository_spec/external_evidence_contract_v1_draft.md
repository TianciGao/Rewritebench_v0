# External Evidence Contract v1 Draft

Status: draft policy for external case evidence references on `feature/case-package-v2-external-schema`

This contract defines the optional retained-static-evidence surface used during case package v2 migration. It does not make static evidence required for clean public v2, move evidence, delete evidence, update reports/results, compute metrics, or authorize retained-evidence adapter implementation.

## Layout

When retained static case evidence is deliberately kept, it may live under:

```text
evidence/cases/<POOL>/<CASE_ID>/
  package_validation_summary.json
  runs_retention.yaml
  retained_controls/
  hard_negative/
  plans/
```

The layout is migration-time or optional retained-artifact context. It is not required in the final clean v2 public case surface. Existing case-local evidence remains compatibility context until a separate migration or cleanup task is authorized.

## Regeneration-first Manifest Shape

Clean v2 manifests should not require static evidence paths. The preferred manifest shape is:

```yaml
evidence_policy:
  static_case_evidence: not_required
  regeneration_policy: regenerable_by_validation_and_report_scripts
  retained_static_artifacts: none
```

Benchmark evidence should be regenerated through validation wrappers, checker configuration, baseline/report scripts, and separately authorized reports/results surfaces.

## Optional evidence_ref Compatibility Shape

If retained static artifacts are deliberately kept during migration, manifests may include compatibility metadata such as:

```yaml
evidence_ref:
  root: evidence/cases/PERF/PERF_0006
  package_validation_summary: evidence/cases/PERF/PERF_0006/package_validation_summary.json
  runs_retention: evidence/cases/PERF/PERF_0006/runs_retention.yaml
  retained_controls: evidence/cases/PERF/PERF_0006/retained_controls/
  hard_negative: evidence/cases/PERF/PERF_0006/hard_negative/
  plans: evidence/cases/PERF/PERF_0006/plans/
```

All paths should be repository-relative and public-safe. `evidence_ref` is optional compatibility metadata; its absence must not fail clean v2 validation when `evidence_policy.static_case_evidence` is `not_required`.

## package_validation_summary Placement

`package_validation_summary.json` belongs under external evidence when it records package validation status rather than intrinsic case source files.

It must not contain task run logs, commit/push metadata, private paths, prompts, credentials, or paper-result claims.

## runs_retention Placement

`runs_retention.yaml` may move to external evidence when case-local evidence is minimized. It records retained evidence roles, do-not-delete mappings, public/private status, and compatibility notes.

Case-local `runs/` must be classified before cleanup. Empty or placeholder-only case-local `runs/` is not retained evidence unless the placeholder explicitly documents retained artifacts stored in that directory. Non-empty, uncertain, retained-evidence-present, sensitive/private, or raw-trace `runs/` remains protected and is not moved or deleted by default.

## retained_controls / hard_negative / plans Roles

- `retained_controls/`: public-safe source/positive/control output references or curated retained control artifacts.
- `hard_negative/`: hard-negative expected rejection evidence and summaries.
- `plans/`: public-safe retained plan evidence and sanitized plan outputs.

These are retained evidence/reference assets, not new user-run output.

Future plan and evidence artifact validation should be implemented as shared repository logic, not as per-case checker code. The planned shared module is `src/sql_rewrite_bench/plan_artifact_validator.py`; it should consume manifest evidence policy, optional retained-artifact metadata, case-local checker configuration, and public-safe retained evidence paths without copying raw private logs, prompts, credentials, or local machine paths into public evidence.

## Distinction From results/retained/

`evidence/cases/` is optional retained case evidence/reference material during migration. `results/retained/` is a curated retained-result/reporting surface only after separate authorization.

Copying evidence into `evidence/cases/` does not by itself create paper results, metric inputs, or report rows. Omitting `evidence/cases/` from clean public v2 does not authorize changing denominators, paper results, official metrics, or reports/results.

## Distinction From runs/user/

`runs/user/<run_id>/` contains local user experiment output. It is ignored by git and must not be promoted to evidence unless a separate retained-evidence task authorizes and maps it.

## Case-local Runs Retention Policy

Case-local `runs/` is classified before any cleanup:

- absent: no cleanup needed
- empty directory: not retained evidence
- placeholder-only: not retained evidence unless the placeholder explicitly documents retained artifacts stored in that directory
- retained evidence present: retention mapping required
- sensitive/private/local-path/raw trace present: private/archive mapping required and no public copy
- manual review required: deletion forbidden until reviewed

Non-empty, uncertain, retained-evidence-present, sensitive/private, or raw-trace case-local `runs/` must not be deleted without:

- retention mapping
- public/private classification
- traceability to retained evidence or archive status
- explicit maintainer approval

## No Deletion Without Retention Mapping

No branch-adoption task may delete retained-evidence-present, sensitive/private, raw-trace, uncertain, or manual-review case-local runs, raw retained evidence, or compatibility evidence directories unless the task explicitly includes retention/archive mapping and approval. Audited empty or placeholder-only case-local runs may be removed only by a separate cleanup task after policy acceptance and protected-boundary checks.
