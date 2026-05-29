# checker_label_only_diagnostics_patch_v0

Verdict: `completed`

This patch adds behavior-preserving local diagnostic visibility for strict checker mismatches where normalized values match positionally but result column labels differ. It does not change `exact_status`, `checker_status`, or `failure_bucket` semantics: label-only rows remain strict mismatches.

## Summary

- Added checker diagnostic fields: `value_exact`, `label_exact`, `label_only_mismatch`, `label_policy`, `label_mismatch_class`, and `value_mismatch_reason`.
- Added mismatch-artifact `label_diagnostics` for fail-visible label-only rows.
- Added local quality-summary visibility through `diagnostic_counts.label_only_mismatch_rows`.
- Kept strict labels as the default policy.
- Kept explicit alias differences strict.
- Did not add generated-expression label inference or any case-local label policy.
- Preserved controlled cross-dialect role gates, including the existing MySQL-source to Spark-target numeric normalization gate.

## Targeted Diagnostic Rerun

Run path: `runs/user/mysql_label_only_diagnostics_patch_check`

The targeted MySQL SQLGlot noop rerun selected the five previously triaged label-only rows:

- `PERF_0062`
- `PORT_0004`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`

All five rows remained `checker_mismatch` with `exact_status=mismatch` and `failure_bucket=mismatch`. All five now report `value_exact=true`, `label_exact=false`, and `label_only_mismatch=true`.

## Boundary

This is a local diagnostic checker visibility patch only. It is not official metrics, timing/speedup, paper results, reports/results migration, retained-evidence promotion, or leaderboard output. No cases, manifests, SQL files, schemas, checker configs, validation scripts, baselines, `case_sets/`, reports/results, denominator scaffolds, paper results, case membership, or raw retained evidence were changed.

## Next Safe Action

Use these diagnostics to decide whether to keep label-only rows fail-visible, document the limitation, or authorize a separate exactness-changing case-local label policy patch with explicit regression coverage.
