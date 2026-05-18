# Wave 002 Batch Plan

## Proposed Wave 002 Scope

Wave 002 should not execute until the maintainer approves the policy questions in `wave002_policy_approval_questions.md`. Under current policy, no deferred wave 001 case is auto-migration-safe because every deferred case carries static public-hygiene risk.

If the policy questions are approved, wave 002 can target the 28 policy-approved deferred cases as a single high-efficiency batch, using no-copy raw evidence boundaries and explicit evidence-retention mapping.

## Target Number Of Cases

- Current auto-migration candidates: 0.
- Policy-approval candidates: 28.
- Recommended target after policy approval: up to 28, with fail-closed skip dossiers for any case whose static package assets do not match the preview metadata.

## Auto-migration Candidates

None under current policy.

## Policy-approval Candidates

`PERF_0002`, `CONS_0031`, `CONS_0034`, `PERF_0009`, `PERF_0010`, `PERF_0011`, `PERF_0012`, `PERF_0014`, `PERF_0015`, `PERF_0016`, `PERF_0018`, `PERF_0020`, `PERF_0021`, `PERF_0022`, `PERF_0023`, `PERF_0025`, `PERF_0026`, `PERF_0036`, `PERF_0038`, `PERF_0043`, `PERF_0044`, `PERF_0047`, `PERF_0050`, `PERF_0053`, `PERF_0063`, `PERF_0065`, `PERF_0066`, and `PERF_0076`.

## Manual-review Exclusions

No wave 001 deferred case is placed into manual review by this selection packet, because governance metadata marks the 28 cases as batchable after policy approval rather than human-review-required. If policy approval is denied, all 28 remain deferred.

## Hard Boundaries

- Do not migrate new cases without separate wave 002 authorization.
- Do not modify `case_sets/`.
- Do not update reports or results.
- Do not change denominator values.
- Do not change paper results.
- Do not compute metrics.
- Do not render paper tables.
- Do not copy raw legacy runs wholesale.
- Do not copy raw logs, stdout/stderr/debug traces, prompt/token/API/model traces, or local-path artifacts.
- Do not modify raw legacy evidence.

## Validation Plan

- Parse all new package YAML and JSON files.
- Run static public-hygiene checks over newly created package files.
- Confirm no `case_sets/`, `reports/`, or `results/` files changed.
- Confirm no raw case-local `runs/` directory was copied.
- Run existing non-mutating case-package validators where applicable.
- Run `python scripts/dev/smoke_ledger_fixtures.py`.
- Run `git diff --check`.

## Suggested Next Codex Prompt Title

`overnight_non_common_core_case_package_standardization_wave_002`
