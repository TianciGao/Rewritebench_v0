# Row Status And Fail-Closed Policy

The official-promotion proposal keeps status rows explicit. Unsupported, missing, mismatched, and invalid rows must not disappear from denominator reporting.

| Status | POCR@planned denominator | POCR@candidate denominator | POCR numerator | Auxiliary counts |
| --- | --- | --- | --- | --- |
| `planned_pocr_eligible` | yes | no, unless candidate-bound | no by itself | planned row count |
| `candidate_bound` | yes | yes | no by itself | candidate-bound row count |
| `no_candidate` | yes, zero contribution | no | no | no-candidate rows |
| `generation_failed` | yes, zero contribution | no | no | generation failures |
| `extraction_failed` | yes, zero contribution | no | no | extraction failures |
| `unsupported_engine` | yes when planned, zero or status-only by route policy | no unless candidate-bound | no | unsupported rows |
| `route_mismatch` | yes, zero contribution | yes if candidate-bound | no | fail-closed mismatch rows |
| `candidate_mismatch` | yes, zero contribution | yes if candidate-bound | no | fail-closed mismatch rows |
| `annotation_missing` | yes, zero contribution | yes if candidate-bound | no | missing annotation rows |
| `annotation_schema_valid` | yes | yes if candidate-bound | no by itself | schema-valid annotation rows |
| `annotation_schema_invalid` | yes, zero contribution after retry window | yes if candidate-bound | no | schema-invalid rows |
| `provider_call_failed` | yes, zero contribution after retry window | yes if candidate-bound | no | provider-failed rows |
| `malformed_json` | yes, zero contribution after retry window | yes if candidate-bound | no | malformed rows |
| `timeout` | yes, zero contribution after retry window | yes if candidate-bound | no | timeout rows |
| `stage_b_supported` | yes | yes if candidate-bound | yes for the supported operation atom | supported atom counts |
| `stage_b_presence_only` | yes | yes if candidate-bound | no | presence-only atom counts |
| `stage_b_insufficient_transformation_evidence` | yes | yes if candidate-bound | no | insufficient-evidence atom counts |
| `not_applicable_no_expected_operation_atoms` | counted separately | counted separately if candidate-bound | no | N.A. row counts |

Fail-closed denominator policy:

- For POCR@planned, no candidate, generation failure, extraction failure, route mismatch, candidate mismatch, annotation missing, and schema-invalid after retry produce `OC_i = 0` with an explicit fail-closed status.
- For POCR@candidate, no-candidate rows are excluded from the denominator, but route mismatch, candidate mismatch, annotation missing, provider failure, malformed JSON, timeout, and schema-invalid rows are retained as explicit candidate-bound fail-closed rows when a candidate identity exists.
- Unsupported or non-eligible rows must be retained as status rows and not silently removed.

Stage A annotation alone is not counted. Stage B transformation-aware validation is required.

No route-level POCR score is emitted in this task. No paper-facing metric is promoted in this task. No global leaderboard is produced.
