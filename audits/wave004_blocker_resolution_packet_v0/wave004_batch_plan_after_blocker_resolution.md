# Wave 004 Batch Plan After Blocker Resolution

## Proposed Wave004 Scope

No wave004 migration batch should run from this packet because zero candidates are policy-unlocked. The current candidate selection after blocker resolution keeps all 97 remaining rows in manual-review, backlog-defer, or orphan/registry-review buckets.

## Recommended Target Size

Recommended wave004 migration target size now: 0 cases.

A future migration wave may be prepared only after a separate manual checker/schema/hard-negative review packet or registry reconciliation packet promotes specific rows into `wave_004_policy_approved_candidate`.

## Candidate IDs To Migrate If Approved

None in this packet.

## Cases To Exclude

Exclude all rows in:

- `wave_004_manual_review_required` until explicit human review resolves checker/schema/hard-negative questions.
- `wave_004_backlog_defer` until missing checker/core package assets are recovered or separately authorized.
- `orphan_or_unregistered_review` until registry reconciliation preview resolves identity and provenance.

## Required Guardrails

Future wave004 work must reuse README template v1 and package_validation_summary schema guard v1. It must not update `case_sets/`, denominators, reports/results, paper results, metrics, paper tables, inventory membership, case membership, raw legacy evidence, or legacy repository files.

## Validation Plan

For any future promoted wave004 rows, run static validation only: YAML/JSON parse, README forbidden-term checks, package_validation_summary disallowed-field checks, public hygiene scan, no raw-runs copy checks, fixture smoke, `git diff --check`, and boundary checks for `case_sets/`, reports, results, denominator, and paper-result changes.

## Stop Conditions

Stop and defer a case if source.sql or positive.sql cannot be located safely, checker/core package assets are absent, registry identity is unresolved, public hygiene cannot be guaranteed, package creation would require DB execution/timing rerun/LLM call, or any case-set/denominator/report/result/paper change would be needed.

## Suggested Next Codex Prompt Title

`wave004_manual_checker_registry_resolution_v0`
