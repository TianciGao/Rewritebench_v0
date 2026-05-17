# STATUS_INFERENCE_POLICY_V0

## What This Policy Is

This developer note summarizes the conservative status-inference policy created after `normalized_status_only_metrics_dryrun_v1`.

The policy separates source-observed normalized fields from possible future inferred fields. It does not authorize official metrics.

## Why Ready/Generated Distinction Matters

Generation Rate is about emitted candidate SQL. `ready=true` is a downstream readiness diagnostic unless a source-specific policy says it proves candidate SQL exists. A future inference overlay may propose `inferred_generated=true`, but it must not overwrite `normalized_generated`.

## Why Exact/Executed Distinction Matters

Result exactness usually depends on execution, but official policy cannot assume that unless the source documents exactness as a post-execution checker result. Any future `inferred_executed=true` must be recorded separately.

## Future Dry-run v2

A future `normalized_status_only_metrics_dryrun_v2` may consume a separately authorized inference overlay. It must remain audit-only unless a later task explicitly authorizes official metrics.

## Non-goals

No timing metrics, paper tables, reports/results updates, denominator changes, paper-result changes, parser-ledger mutation, or normalization-overlay mutation are part of this policy.
