FUTURE PROMPT — DO NOT EXECUTE NOW

This prompt is a future planning/implementation prompt draft. Do not execute it as part of the overnight investigation bundle.

Hard boundaries:
- Do not modify the legacy repository.
- Do not run DB engines, LLM calls, timing workloads, or validation scripts against engines.
- Do not change Common-core membership, denominator values, paper results, reports/results, or raw legacy evidence.
- Do not use `git add .`.

# Legacy Script Redevelopment Detailed Design

Goal: Turn the read-only legacy script inventory into a detailed public workbench redevelopment design.

Inputs:
- `audits/overnight_investigation_bundle/legacy_script_reference_inventory.csv`
- repository specs for evidence ledger, metrics contract, and public runner output policy.

Scope:
- Propose future module boundaries and script entrypoints.
- Identify wrappers vs refactors vs private/archive exclusions.
- Do not create implementation files under `scripts/` or `src/`.

Abort if the task requires metric computation, DB execution, or copying legacy scripts wholesale.
