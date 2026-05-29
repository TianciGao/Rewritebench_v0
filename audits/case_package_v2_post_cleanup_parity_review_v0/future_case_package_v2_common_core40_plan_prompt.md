# Future Prompt: case_package_v2_common_core40_conversion_plan_v0

Repository:

- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify `main`.
- Do not inspect or modify the legacy repo.

Task title:

`case_package_v2_common_core40_conversion_plan_v0`

This is a branch-only read-only planning task.

This is NOT writable case conversion.
This is NOT cleanup execution.
This is NOT retained-evidence deletion.
This is NOT DB/checker execution.
This is NOT official metric computation.
This is NOT reports/results migration.
This is NOT denominator update.
This is NOT case_sets update.
This is NOT global leaderboard creation.

## Goal

Plan a Common-core 40 case-package v2 conversion using the five-case pilot as the accepted functional v2 template.

The five-case pilot is acceptable for functional v2 planning because:

- all clean-template-required v2 assets are present
- static v2 validator passes for all five pilot cases
- profile-first schema resolution is supported
- direct SQL paths are canonical
- checker and validation wrappers are canonical
- witness/evidence references are canonical
- the first safe compatibility-reference cleanup removed nested SQL compatibility paths and copied case-local notes

The pilot is not yet clean-template-minimal. The plan must carry these cleanup tracks as separate non-blocking work:

- retained evidence mapping for case-local `evidence/`
- retained-runs cleanup or mapping for case-local `runs/`
- schema engine copy cleanup after runner/schema-profile acceptance
- metadata source-of-truth review
- data fixture and witness/data policy review
- old validation engine-specific script cleanup after shared logic/caller audit
- `PORT_0003` dialect-variant manual review

## Required Planning Scope

Plan conversion only. Do not convert cases.

The plan must cover:

- which Common-core 40 cases are already v2-compatible or close to v2-compatible
- folder-ordered conversion phases for manifest, sql, schema, checker, validation, witness, evidence, metadata, notes, runs, README, and validator
- schema package reuse or creation strategy
- evidence copy-first strategy
- retained evidence and runs mapping strategy
- validator and resolver compatibility assumptions
- batch size and ordering
- stop conditions
- protected surfaces that must remain unchanged
- exact future writable pilot prompt

## Hard Boundaries

Do not:

- modify case files
- modify schemas
- modify evidence
- delete runs
- delete retained evidence
- modify case_sets
- modify inventory
- modify reports/results
- change denominators
- change paper results
- compute official metrics
- run DB/checker execution
- render paper tables
- create leaderboard output

## Expected Output

Create an audit directory:

`audits/case_package_v2_common_core40_conversion_plan_v0/`

Include:

- Common-core 40 v2 planning summary
- per-case readiness matrix
- folder-order conversion plan
- schema externalization plan
- evidence/runs mapping plan
- cleanup carry-forward plan
- stop-condition matrix
- future writable conversion prompt
- summary JSON
- command log
