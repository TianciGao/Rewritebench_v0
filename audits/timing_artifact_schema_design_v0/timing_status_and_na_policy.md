# Timing Status And N.A. Policy

Timing artifacts must preserve why rows are untimed or ineligible. Rows must not disappear from the performance surface just because they cannot contribute to `M_r`.

## Timing Status Values

| Status | Meaning | Speedup |
| --- | --- | --- |
| `not_requested` | Timing was not requested for this local run. | `null` |
| `not_eligible` | Row failed the exact gate or role/support gate. | `null` |
| `timed` | Source and candidate completed all requested measured samples. | present if medians are positive |
| `timeout` | At least one side timed out under policy. | `null` |
| `partial_failure` | Some samples exist but requested complete paired samples were not collected. | `null` by default |
| `failed_internal` | Timing infrastructure failed independently of SQL execution result. | `null` |
| `skipped_policy` | Run policy deliberately skipped timing despite eligibility. | `null` |

## Timing N.A. Reasons

Recommended `timing_na_reason` values:

- `generated_missing`
- `preflight_failed`
- `source_execution_failed`
- `candidate_execution_failed`
- `checker_mismatch`
- `label_only_mismatch`
- `unsupported_fail_closed`
- `not_selected`
- `not_requested`
- `timing_timeout`
- `timing_partial_failure`
- `timing_internal_failure`
- `policy_skipped`
- `non_positive_median`

## Failure Visibility Requirements

- Generated-missing rows remain in the denominator chain with `timing_eligible=false`.
- Preflight failures remain visible and timing-ineligible.
- Source execution failures remain visible and timing-ineligible.
- Candidate execution failures remain visible and timing-ineligible.
- Checker mismatches remain visible and timing-ineligible.
- Label-only mismatches remain strict mismatches and timing-ineligible under current policy.
- Unsupported/fail-closed rows remain visible and timing-ineligible.
- Timeouts do not become zero speedup.
- Partial timing samples do not become a speedup unless a later policy explicitly authorizes partial-sample interpretation.

## Timeout Status Values

| Timeout Status | Meaning |
| --- | --- |
| `none` | No timeout occurred. |
| `source_timeout` | Source timing timed out. |
| `candidate_timeout` | Candidate timing timed out. |
| `both_timeout` | Both source and candidate timed out. |
| `partial_timeout` | At least one repetition timed out while others completed. |

## Label-Only Policy

Under the current strict checker label policy, `label_only_mismatch=true` is diagnostic visibility only. It does not satisfy exactness and therefore does not qualify for timing or performance metrics.
