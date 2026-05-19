# Case-local Runs Reality Audit And V2 Policy Refinement

Task: `case_package_v2_runs_reality_audit_and_policy_update_v0`

Date: 2026-05-19

Branch: `feature/case-package-v2-external-schema`

## Purpose And Scope

This branch-only audit inspected the actual current state of case-local `runs/` directories under `cases/<POOL>/<CASE_ID>/` and refined v2 policy where the evidence showed that current `runs/` directories are empty or placeholder-only rather than retained evidence payloads.

No case package files, `runs/` directories, evidence files, schemas, case sets, inventory, reports, results, denominators, paper results, DB/checker outputs, official metrics, or leaderboard outputs were modified or deleted.

## Counts

- Total cases inspected: 100
- `runs/` absent: 1
- `runs/` empty: 0
- `runs/` placeholder-only: 99
- `runs/` retained-evidence-present: 0
- `runs/` sensitive/private/raw trace: 0
- `runs/` manual-review: 0

## Classification Result

The current feature branch has 100 case-package directories. Ninety-nine have case-local `runs/` containing a single tracked `README.md` placeholder or retention note. One case, `PORT_0008`, has no case-local `runs/` directory.

The audit found no current case-local `runs/` directory containing result outputs, plan outputs, hard-negative artifacts, checker/control outputs, method/baseline outputs, timing or execution artifacts, raw logs, debug traces, sensitive/private traces, local-path-heavy artifacts, or ambiguous non-placeholder files.

## Implication For V2 Policy

The existing D005 protection remains correct for non-empty, uncertain, retained-evidence-present, sensitive/private, or raw trace `runs/` directories. However, treating every current case-local `runs/` directory as retained evidence is overbroad for v2 cleanup because the current branch overwhelmingly contains placeholder-only markers.

Refined v2 policy should distinguish:

- absent `runs/`: no cleanup needed
- empty `runs/`: not retained evidence
- placeholder-only `runs/`: not retained evidence unless the placeholder explicitly documents retained artifacts stored in that directory
- retained-evidence-present `runs/`: retention mapping required before deletion
- sensitive/private/raw trace `runs/`: private/archive mapping required; do not public-copy
- manual-review `runs/`: deletion forbidden until reviewed

## Recommended Cleanup Policy

A future cleanup task may delete only audited empty or placeholder-only case-local `runs/` directories after policy acceptance and protected-boundary checks. It must not delete non-empty retained-evidence candidates, sensitive/private/raw traces, manual-review directories, case-local evidence, schemas, reports/results, denominator inputs, paper-result inputs, or any leaderboard/metric output.

New user-run outputs must continue to live under top-level `runs/user/<run_id>/`, not inside case-local `runs/`.

## Exact Next Safe Action

Authorize `case_package_v2_empty_runs_cleanup_v0` only to delete audited empty or placeholder-only case-local `runs/` directories after accepting the refined v2 policy, with no retained-evidence deletion, evidence deletion, DB/checker execution, official metrics, protected benchmark-surface changes, or leaderboard output.
