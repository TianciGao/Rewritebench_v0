# Wave 004 Batch Plan

## Recommended Target Size

Recommended wave 004 migration target size: 0 cases until additional manual/policy resolution is completed. The current selection has no auto or policy-approved migration candidates.

## Recommended Candidate IDs

No case IDs are recommended for immediate wave 004 migration under current guardrails.

## Excluded / Manual-Review Cases

Manual-review rows (13): PERF_0001, PERF_0003, PERF_0004, PERF_0005, PERF_0046, PERF_0048, CONS_0001, CONS_0002, CONS_0003, CONS_0004, PORT_0001, LONGTAIL_0001, LONGTAIL_0002.

Backlog-defer rows (77): PERF_0078, PERF_0080, PERF_0081, PERF_0083, PERF_0084, PERF_0085, PERF_0086, PERF_0090, PERF_0091, PERF_0093, PERF_0094, PERF_0095, PERF_0096, PERF_0097, PERF_0101, PERF_0102, PERF_0103, PERF_0104, PERF_0105, PERF_0106, PERF_0107, PERF_0108, PERF_0109, CONS_0006, CONS_0008, CONS_0013, CONS_0014, CONS_0015, CONS_0016, CONS_0017, CONS_0018, CONS_0019, CONS_0020, CONS_0021, CONS_0022, CONS_0023, CONS_0025, CONS_0026, CONS_0027, CONS_0028, CONS_0029, CONS_0030, CONS_0032, CONS_0033, CONS_0035, CONS_0038, CONS_0039, CONS_0040, PORT_0009, PORT_0010, PORT_0011, PORT_0014, PORT_0015, PORT_0016, PORT_0017, PORT_0018, PORT_0019, PORT_0020, PORT_0021, PORT_0023, PORT_0026, PORT_0027, PORT_0028, LONGTAIL_0003, LONGTAIL_0004, LONGTAIL_0005, LONGTAIL_0007, LONGTAIL_0008, LONGTAIL_0009, LONGTAIL_0010, LONGTAIL_0014, LONGTAIL_0015, LONGTAIL_0016, LONGTAIL_0018, LONGTAIL_0019, LONGTAIL_0020, LONGTAIL_0021.

Orphan/unregistered review rows (7): PERF_0079, PERF_0087, PERF_0092, PERF_0100, PORT_0007, LONGTAIL_0006, LONGTAIL_0017.

## Policy Guardrails To Reuse

Wave 004 must reuse the wave 002/003 guardrails: do not copy raw runs wholesale, do not copy raw logs/stdout/stderr/debug payloads, do not copy prompt/token/API traces, archive-map or exclude unsafe run evidence, use `evidence_not_retained` only when core source/positive/checker assets are complete, and never change `case_sets/`, denominators, reports/results, paper results, metrics, or raw legacy evidence.

## README Template / Schema Guard Requirements

Any future migrated package must use `repository_spec/case_readme_public_template_v1.md` and `repository_spec/package_validation_summary_schema_v1.md`. Case-local `package_validation_summary.json` must not include migration-task or repository-global fields.

## Validation Plan

Run static-only validation: package layout checks, README forbidden-term checks, package-validation summary schema checks, YAML/JSON parse checks, raw-runs and raw-log absence checks, `python scripts/dev/smoke_ledger_fixtures.py`, and `git diff --check`. Do not run DB engines, timing workloads, LLM calls, or metric computation.

## Stop Conditions

Stop if a candidate requires DB execution, timing rerun, LLM calls, case-set or denominator changes, paper-result changes, raw legacy evidence modification, raw log/prompt/token evidence, or manual semantic approval that has not been documented.

## Suggested Next Codex Prompt Title

`wave004_blocker_resolution_missing_checker_orphan_review_v0`
