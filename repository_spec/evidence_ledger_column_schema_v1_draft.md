# Evidence Ledger Column Schema v1 Draft

Status: draft column model, not implementation-authorizing

Purpose: define the planned evidence ledger columns before retained-evidence adapters, metrics computation, paper rendering, reproduction CLI, or public runner outputs are implemented.

This draft does not parse production retained evidence, compute metrics, create scripts, create source implementation files, copy reports/results, update denominator values, change paper results, change case membership, or modify raw legacy evidence.

## Column Model

The ledger is a typed long-format table. Every row must identify its `record_type`, evidence source, row grain, and denominator boundary when applicable.

| Field | Description | Type | Required or optional | Nullable policy | Allowed values if constrained | Applicable record types | Denominator effect | Metrics can read later | Diagnostic/support only |
|---|---|---|---|---|---|---|---|---|---|
| `record_id` | Stable ledger row identifier. | string | required | not nullable | stable adapter or fixture ID | all | no direct effect | yes for joins | no |
| `record_type` | Typed row discriminator. | enum | required | not nullable | `control_cell`; `rewrite_candidate_cell`; `plan_observability_artifact`; `portability_candidate_cell`; `verifier_support_pair`; `retained_summary_artifact`; `user_run_candidate_cell` | all | separates denominator families | yes | no |
| `case_id` | Common-core case identifier. | string | required for case-scoped rows | nullable for mixed summaries | Common-core case ID | all except mixed `retained_summary_artifact` | identifies membership only | yes | no |
| `pool` | Case pool. | enum | required when `case_id` is set | nullable for mixed summaries | `PERF`; `CONS`; `PORT`; `LONGTAIL` | case-scoped rows | no direct effect | yes | no |
| `case_set` | Release case-set namespace. | enum | required | not nullable | `common_core_v0` for public v0 scope | all | selects membership namespace | yes | no |
| `denominator_id` | Planned denominator or control scaffold identifier. | string | required for denominator-scoped rows | nullable for support-only rows | `track_a_same_engine:*`; `control:*`; future approved IDs | `control_cell`; `rewrite_candidate_cell`; benchmark-scoped `user_run_candidate_cell`; optional future `portability_candidate_cell` | denominator join key | yes | no |
| `engine` | Engine observed by the row. | enum | required for engine-scoped rows | nullable for non-engine support rows | `postgres`; `mysql`; `spark` | engine-scoped rows | part of Track A and controls | yes | no |
| `source_engine` | Source engine for paired portability or retention rows. | enum | optional | nullable | `postgres`; `mysql`; `spark` | `portability_candidate_cell`; paired performance support rows | paired generalization context | yes | no |
| `target_engine` | Target engine for portability/generalization rows. | enum | required for target-engine portability rows | nullable otherwise | `postgres`; `mysql`; `spark` | `portability_candidate_cell` | portability denominator context | yes | no |
| `rewrite_method` | Public-facing rewrite method name. | string | required for method candidate rows | nullable for controls and summaries | approved method label | `rewrite_candidate_cell`; `portability_candidate_cell`; `user_run_candidate_cell` | method slice only | yes | no |
| `route` | Evidence route. | enum | required | not nullable | `source`; `positive`; `hard_negative`; `same_engine_rewrite`; `portability`; `plan_observability`; `verifier_support`; `summary` | all | route boundary | yes | no |
| `method_role` | Role-aware method or support label. | enum/string | required | not nullable | `control`; `direct_llm`; `repair_1`; `sqlglot`; `calcite_hep`; `r_bot`; `verifier_support`; `retained_legacy_reference`; `user_candidate`; future approved roles | all | metric slice only | yes | no |
| `control_route` | Control route for source/positive/hard-negative rows. | enum | required for `control_cell` | nullable otherwise | `source`; `positive`; `hard_negative` | `control_cell` | joins `controls_360.csv` | yes for control reports | no |
| `candidate_id` | Candidate or control identifier. | string | required for candidate/control rows | nullable for summary-only rows | stable deterministic ID | `control_cell`; `rewrite_candidate_cell`; `portability_candidate_cell`; `user_run_candidate_cell` | prevents row collapse | yes | no |
| `artifact_id` | Artifact-level identifier. | string | required for artifact rows | nullable otherwise | stable deterministic artifact ID | `plan_observability_artifact`; `retained_summary_artifact` | no denominator effect | yes for support joins | yes |
| `support_pair_id` | Verifier support pair identifier. | string | required for verifier rows | nullable otherwise | stable SQL-pair support ID | `verifier_support_pair` | no denominator effect | yes for semantic support | yes |
| `source_sql_path` | Repository-relative source SQL path. | string/path | required for candidate/control rows | nullable for summaries | repository-relative path | `control_cell`; `rewrite_candidate_cell`; `portability_candidate_cell`; `user_run_candidate_cell` | no direct effect | yes | no |
| `candidate_sql_path` | Candidate/control/user SQL path. | string/path | required when SQL exists | nullable with explicit status | repository-relative or output-root path | candidate/control/user rows | no direct effect | yes | no |
| `generated` | Whether candidate SQL was emitted. | boolean/status | required for candidate rows | nullable for support-only rows | `true`; `false`; `unknown`; `not_applicable` | `rewrite_candidate_cell`; `portability_candidate_cell`; `user_run_candidate_cell` | supports Generation Rate | yes | no |
| `ready` | Whether row reached downstream readiness gate. | boolean/status | required for candidate rows after parsing | nullable for support-only rows | `true`; `false`; `unknown`; `not_applicable` | candidate rows | readiness diagnostic only | maybe | yes |
| `executed` | Whether execution happened. | boolean/status | required for execution-relevant rows | nullable for pure summaries | `true`; `false`; `unknown`; `not_applicable` | controls and candidate rows | supports execution denominator slice | yes | no |
| `exact` | Whether correctness gate passed. | boolean/status | required after checker/result parsing | nullable for support-only rows | `true`; `false`; `unknown`; `not_applicable` | controls and candidate rows | correctness slice only | yes | no |
| `timed` | Whether usable timing evidence exists. | boolean/status | required for performance-relevant rows | nullable for support-only rows | `true`; `false`; `unknown`; `not_applicable` | candidate rows | performance slice only | yes | no |
| `result_status` | Normalized row outcome. | enum | required after parsing | nullable for pending support summaries | `pass`; `fail`; `mismatch`; `unsupported`; `not_applicable`; `unknown`; `timing_missing`; `target_timing_missing`; `evidence_not_retained`; `manual_review_required`; `blocked`; `checker_rejected`; `not_run` | non-summary rows | reporting state only | yes | no |
| `failure_stage` | Stage where failure or missingness occurred. | enum | optional | nullable for success rows | `generation`; `parse`; `preflight`; `execution`; `checker`; `plan_collection`; `timing`; `artifact_collection`; `not_applicable`; `unknown` | candidate/control/artifact rows | no direct effect | yes for diagnostics | yes |
| `failure_type` | Stable failure bucket. | enum/string | optional | nullable for success rows | approved bucket or `unknown` | candidate/control/artifact rows | no direct effect | yes for diagnostics | yes |
| `parse_status` | SQL extraction or parse status. | enum | optional until parser exists | nullable for support-only rows | `parsed`; `not_parsed`; `unknown`; `not_applicable` | candidate/user rows | diagnostic only | maybe | yes |
| `checker_status` | Checker or expected-rejection status. | enum | required where checker applies | nullable where not applicable | `pass`; `fail`; `reject_expected`; `reject_unexpected`; `not_run`; `not_applicable`; `unknown` | controls and candidate rows | correctness support | yes | no |
| `plan_available` | Whether public-safe plan evidence exists. | boolean/status | required for plan rows | nullable elsewhere | `true`; `false`; `unknown`; `not_applicable` | `plan_observability_artifact`; plan-linked rows | support only | maybe for Attribution Coverage | yes |
| `plan_artifact_path` | Public-safe plan path or archive reference. | string/path | required when `plan_available=true` | nullable otherwise | repository-relative path; output-root path; archive reference | plan rows and plan-linked rows | no speedup effect | maybe | yes |
| `latency_ms` | Timing value in milliseconds. | decimal | optional | nullable | positive number or null | performance-eligible candidate rows | performance slice only | yes after authorization | no |
| `speedup_ratio` | Speedup ratio value. | decimal | optional | nullable | positive number or null | performance-eligible candidate rows | performance slice only | yes after authorization | no |
| `timing_eligible` | Whether timing interpretation is allowed. | boolean/status | required before performance reporting | nullable for support rows | `true`; `false`; `unknown`; `not_applicable` | candidate rows | performance eligibility gate | yes | no |
| `evidence_source` | Source class for the row. | enum | required | not nullable | `synthetic_fixture`; `canonical_case_package`; `retained_legacy_report`; `retained_legacy_run`; `adapter_import`; `user_run`; `manual_summary` | all | traceability only | yes | no |
| `retained_artifact_path` | Supporting retained artifact path or reference. | string/path | required for retained/support rows | nullable for synthetic-only rows with notes | repository path; legacy reference; archive reference; fixture path | all retained/support rows | traceability only | yes | yes |
| `status` | High-level fixture or ledger status. | enum/string | required | not nullable | `generated`; `ready`; `executed`; `exact`; `mismatch`; `failed`; `N.A.`; `unsupported`; `unknown`; other approved status | all | reporting state only | yes | no |
| `na_reason` | Reason for `N.A.` or unavailable state. | enum/string | required when status is `N.A.` or field is unavailable | nullable otherwise | `unsupported`; `not_applicable`; `unknown`; `verifier_unknown`; `timing_missing`; `target_timing_missing`; `evidence_not_retained`; `manual_review_required`; `blocked` | all | explains exclusion only | yes for report caveats | yes |
| `notes` | Human-readable caveat. | string | required for fixtures and unresolved rows | not nullable for fixture rows | free text without secrets or local paths | all | no direct effect | yes for audit | yes |

## Implementation Boundary

This draft is a schema contract for future validators and adapters. It does not authorize materializing production ledgers, parsing retained evidence, computing metrics, or rendering paper tables.
