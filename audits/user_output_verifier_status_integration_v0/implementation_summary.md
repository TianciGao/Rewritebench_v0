# Implementation Summary

## Files changed

- `src/sql_rewrite_bench/user_output.py`
- `src/sql_rewrite_bench/user_output_schema.py`
- `tests/user_entry/test_user_output.py`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

## Behavior added

- User-output export now detects source-run `verifier/` artifacts.
- Existing source verifier artifacts are copied to `output/results/<run_id>/verifier/`.
- `verifier_status.json` is normalized or created with local-only boundary fields.
- `verifier_summary.md` distinguishes `N.A.`, `coverage_limited`, and `computed_local_support`.
- `no_verifier_support` is displayed as a verifier-support status, not a method failure bucket.

## N.A. behavior

Runs with no verifier artifacts still receive an explicit verifier placeholder:

- `semantic_equivalence_rate_status = N.A.`
- `reason = formal_verifier_evidence_missing`
- `official_SER = false`

## Coverage-limited behavior

Runs with coverage-limited verifier artifacts export tool summaries including attempted, decidable, equivalent, non-equivalent, unknown, timeout, unsupported, `no_verifier_support`, and tool-error counts.

## Compatibility

The local metrics and tag-slice export paths are unchanged. The exporter still does not invoke adapters, DB execution, checker execution, timing, LLM calls, verifier tools, official metrics, paper rendering, or Repair-1.
