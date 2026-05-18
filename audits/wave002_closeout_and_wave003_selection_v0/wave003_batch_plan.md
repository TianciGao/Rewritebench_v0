# Wave 003 Batch Plan

## Recommended Target Size

Target 30 cases in one bounded wave. The selected queue is intentionally limited to complete-core candidates that can reuse wave 002 policy guardrails.

## Recommended Candidate IDs

- PERF_0027
- PERF_0028
- PERF_0030
- PERF_0031
- PERF_0032
- PERF_0037
- PERF_0039
- PERF_0040
- PERF_0041
- PERF_0042
- PERF_0045
- PERF_0049
- PERF_0051
- PERF_0055
- PERF_0057
- PERF_0058
- PERF_0059
- PERF_0060
- PERF_0061
- PERF_0064
- PERF_0067
- PERF_0068
- PERF_0069
- PERF_0070
- PERF_0071
- PERF_0072
- PERF_0073
- PERF_0074
- PERF_0075
- PORT_0006

## Excluded / Manual-review Cases

Manual-review rows remain excluded from the automated wave: PERF_0001, PERF_0003, PERF_0004, PERF_0005, PERF_0046, PERF_0048, CONS_0001, CONS_0002, CONS_0003, CONS_0004, PORT_0001, LONGTAIL_0001, LONGTAIL_0002.

Orphan or unregistered rows remain excluded pending registry reconciliation: PERF_0079, PERF_0087, PERF_0092, PERF_0100, PORT_0007, LONGTAIL_0006, LONGTAIL_0017.

Backlog-defer rows remain governed but not selected for wave 003 because they are outside the complete-core/high-throughput target or have weaker package assets.

## Policy Guardrails to Reuse from Wave 002

- Static-inferred hard-negative reason may be used only with `needs_review` marking and no paper-facing approval.
- Validation scripts may be retained as legacy assets with output-policy caveats, but not executed.
- Spark/local-path/raw plan artifacts must be sanitized or archive-mapped; raw local-path artifacts must not be copied.
- Missing retained evidence may be represented as `evidence_not_retained` when core assets are complete.
- README template v1 and package_validation_summary schema guard v1 are required.
- Raw logs, prompt/token/API traces, stdout/stderr/debug payloads, and raw legacy run directories remain forbidden.

## README and Schema Requirements

Use `repository_spec/case_readme_public_template_v1.md` for every README and `repository_spec/package_validation_summary_schema_v1.md` for every case-local `evidence/package_validation_summary.json`.

## Validation Plan

- Static YAML/JSON parse for all new package metadata and evidence indexes.
- README forbidden-term and required-section checks.
- Package-validation-summary schema guard checks.
- Public hygiene scan for raw logs, private traces, and raw local paths.
- Confirm no `case_sets/`, denominator, reports/results, paper-result, Common-core package, metric, or paper-table changes.
- Run `python scripts/dev/smoke_ledger_fixtures.py`.
- Run `git diff --check`.

## Stop Conditions

Stop and defer any case that needs DB execution, timing reruns, LLM calls, raw log publication, prompt/token/API trace publication, raw local-path artifact publication, `case_sets/` changes, denominator changes, reports/results updates, paper-result changes, or manual semantic approval.

## Suggested Next Codex Prompt Title

`overnight_non_common_core_case_package_standardization_wave_003`
