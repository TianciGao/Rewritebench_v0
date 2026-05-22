# Timing Policy Schema

The timing policy artifact records how a future local timing diagnostic collected or would collect timing samples. It makes timing runs comparable within their local claim boundary without turning them into official paper evidence.

Suggested local path:

```text
runs/user/{run_name}/timing/timing_policy.json
```

## Required Fields

| Field | Type | Notes |
| --- | --- | --- |
| `schema_version` | string | Suggested value: `timing_policy_schema_v0`. |
| `timing_policy_id` | string | Stable identifier referenced by timing rows. |
| `description` | string | Human-readable policy summary. |
| `exact_gated` | boolean | Must be `true` for the current design. |
| `allowed_timing_scopes` | array[string] | For example `same_engine`, `cross_engine_target`. |
| `warmup_count` | integer | Proposed default from alignment audit: `1`. |
| `measured_repetitions` | integer | Proposed default from alignment audit: `5`. |
| `timeout_seconds` | number | Engine/route configurable. |
| `pairing_policy` | string | Source/candidate must be paired in the same row/run context. |
| `execution_order_policy` | string | `source_then_candidate`, `candidate_then_source`, or `alternating`; open for human confirmation. |
| `cache_policy` | string | Must be recorded, not assumed. |
| `connection_session_policy` | string | Connection/session reuse/reset policy. |
| `schema_setup_policy` | string | Schema load/reuse policy for the timed run. |
| `transaction_policy` | string | Transaction isolation/commit/rollback behavior where applicable. |
| `retry_policy` | string | Defaults should avoid hiding failures; retries must be visible. |
| `partial_sample_policy` | string | How partial source/candidate sample failures are reported. |
| `statistic` | string | Proposed metric input statistic: `median_ms`. |
| `sample_retention` | string | Full source/candidate sample arrays retained. |
| `engine_specific_options` | object | Engine knobs with redacted secrets. |
| `claim_boundary` | string | `local_diagnostic_only` for this phase. |

## Proposed Defaults

| Setting | Proposed Default | Rationale |
| --- | --- | --- |
| exact gate | required | Latest-paper performance interpretation is exact/timed gated. |
| warmups | `1` source/candidate pair | Low-cost local diagnostic default; configurable later. |
| measured repetitions | `5` source/candidate pairs | Enough to retain sample arrays and median without long runs. |
| statistic | median runtime in ms | Stable against single-sample noise. |
| speedup basis | source median / candidate median | Matches D032 and latest alignment audit. |
| sample retention | full arrays | Future metrics and audits need raw sample visibility. |
| timeout handling | nullable speedup with explicit N.A. reason | Timeouts are not zero speedup. |
| cache/session | record explicit policy | Do not claim cold/warm comparability without metadata. |

## Partial Failure Policy

Recommended default: a row is `timing_status=partial_failure` if either side has fewer successful measured samples than requested. The row must keep available samples, set `speedup_ratio=null`, and report a specific `timing_na_reason` unless a future policy explicitly authorizes partial-sample metrics.

## Route Mixing Guard

The policy must not aggregate across routes. `route_id`, `method_id`, `timing_policy_id`, `engine`, and `denominator_id` must be part of all future summary group keys.
