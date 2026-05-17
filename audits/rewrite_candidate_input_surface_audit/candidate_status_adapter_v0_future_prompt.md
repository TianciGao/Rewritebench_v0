# FUTURE PROMPT - DO NOT EXECUTE NOW

Task title:
candidate_status_adapter_v0 release-summary-only non-timing status fill

This is a future bounded adapter task. Do not execute this prompt without explicit maintainer authorization.

## Authorized Scope To Request Later

- Adapter name: `candidate_status_adapter_v0`
- Allowed record type: `rewrite_candidate_cell`
- Allowed method scope: the five Track-A same-engine methods already present in `rewrite_candidate_adapter_v0`
- Allowed fields: non-timing candidate status fields only, such as `generated`, `ready`, `executed`, `exact`, `result_status`, `failure_stage`, `failure_type`, `parse_status`, `checker_status`, `evidence_source`, and `retained_artifact_path`
- Disallowed fields: `timed`, `latency_ms`, `speedup_ratio`, `timing_eligible`, aggregate metrics, paper table rows
- Required safety: `metric_input_authorized=false` unless a later task explicitly changes that

## Inputs To Consider Later

- `audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv`
- `case_sets/common_core_v0/cases.csv`
- `case_sets/common_core_v0/denominator_same_engine_120.csv`
- `inventory/case_registry.csv`
- Release-repo retained-evidence maps as manifests only, if the maintainer authorizes them for this bounded status adapter

## Boundaries

- No metrics computation.
- No Generation Rate computation.
- No Execution Coverage Rate computation.
- No Result Consistency Rate computation.
- No timing fields.
- No paper rendering.
- No production retained-evidence parsing unless separately authorized.
- No legacy raw evidence unless separately authorized.
- No reports/results mutation.
- No denominator changes.
- No paper result changes.
- No raw legacy evidence changes.

## Fail-closed Rules

- If a release summary does not prove row grain, keep the scaffold row as `evidence_not_adapted_yet`.
- If a method route mixes source, repair, portability, or timing artifacts, require manual review.
- If a row cannot be joined to the Track-A denominator, fail validation.
- If any output attempts to set `metric_input_authorized=true`, fail validation.

## Expected Output Shape

The output should remain an audit artifact, not an official production ledger under `results/retained`. It should be validated by `scripts/dev/validate_ledger_csv.py` and documented as non-metric, non-paper evidence.

## Suggested Next Safe Action

Before implementing this future adapter, prepare a short authorization packet listing exact release-repo input files, fields to fill, fields to keep `N.A.`, validation gates, and expected failure behavior.
