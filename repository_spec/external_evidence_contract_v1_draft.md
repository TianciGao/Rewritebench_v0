# External Evidence Contract v1 Draft

Status: draft policy for external case evidence references on `feature/case-package-v2-external-schema`

This contract defines an external evidence strategy for case package v2. It does not move evidence, delete evidence, update reports/results, compute metrics, or authorize retained-evidence adapter implementation.

## Layout

External case evidence should live under:

```text
evidence/cases/<POOL>/<CASE_ID>/
  package_validation_summary.json
  runs_retention.yaml
  retained_controls/
  hard_negative/
  plans/
```

The layout is copy-first and reference-first. Existing case-local evidence remains compatibility context until a separate migration task is authorized.

## evidence_ref Manifest Shape

Recommended manifest shape:

```yaml
evidence_ref:
  root: evidence/cases/PERF/PERF_0006
  package_validation_summary: evidence/cases/PERF/PERF_0006/package_validation_summary.json
  runs_retention: evidence/cases/PERF/PERF_0006/runs_retention.yaml
  retained_controls: evidence/cases/PERF/PERF_0006/retained_controls/
  hard_negative: evidence/cases/PERF/PERF_0006/hard_negative/
  plans: evidence/cases/PERF/PERF_0006/plans/
```

All paths should be repository-relative and public-safe.

## package_validation_summary Placement

`package_validation_summary.json` belongs under external evidence when it records package validation status rather than intrinsic case source files.

It must not contain task run logs, commit/push metadata, private paths, prompts, credentials, or paper-result claims.

## runs_retention Placement

`runs_retention.yaml` may move to external evidence when case-local evidence is minimized. It records retained evidence roles, do-not-delete mappings, public/private status, and compatibility notes.

Case-local `runs/` remains legacy retained evidence and is not moved or deleted by default.

## retained_controls / hard_negative / plans Roles

- `retained_controls/`: public-safe source/positive/control output references or curated retained control artifacts.
- `hard_negative/`: hard-negative expected rejection evidence and summaries.
- `plans/`: public-safe retained plan evidence and sanitized plan outputs.

These are retained evidence/reference assets, not new user-run output.

## Distinction From results/retained/

`evidence/cases/` is case evidence/reference material. `results/retained/` is a curated retained-result/reporting surface only after separate authorization.

Copying evidence into `evidence/cases/` does not by itself create paper results, metric inputs, or report rows.

## Distinction From runs/user/

`runs/user/<run_id>/` contains local user experiment output. It is ignored by git and must not be promoted to evidence unless a separate retained-evidence task authorizes and maps it.

## Case-local Runs Retention Policy

Case-local `runs/` must not be deleted without:

- retention mapping
- public/private classification
- traceability to retained evidence or archive status
- explicit maintainer approval

## No Deletion Without Retention Mapping

No branch-adoption task may delete case-local runs, raw retained evidence, or compatibility evidence directories unless the task explicitly includes retention mapping and approval.
