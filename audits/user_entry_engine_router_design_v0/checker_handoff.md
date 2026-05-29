# Checker Handoff

## Current Checker

Current module: `src/sql_rewrite_bench/local_result_checker.py`.

Current entrypoint: `run_local_checker(...)`.

The checker compares local JSONL execution artifacts. It is not an executor and not a formal SQL verifier.

## Engine Artifact Inputs

The future engine router should pass checker only when both source and candidate execution succeeded and both JSONL paths are present:

- `source_result_path`
- `candidate_result_path`
- case directory or resolved checker config paths
- checker output directory under `runs/user/{run_name}/workspaces/{case_id}/{engine}/checker/`

Checker config inputs:

- `checker/checker.yaml`
- `checker/normalization.yaml`
- `checker/compare_config.yaml`

Future code should prefer resolved paths from `case_package_resolver.py` over reconstructing paths in `user_run.py`.

## Checker Outputs

- `checker_status`
- `exact_status`
- `checker_failure_class`
- `mismatch_artifact_path`
- `failure_bucket`
- notes

## Boundaries

`local_result_checker.py` must not:

- execute SQL
- set up schemas
- run adapters
- perform candidate preflight
- collect timing
- compute speedup
- compute official metrics
- update reports/results
- promote retained evidence
- act as a formal semantic-equivalence verifier

## Exact/Mismatch Handoff

- `exact` and `mismatch` are local diagnostic outcomes over the current JSONL artifacts.
- `checker_failed` and `checker_config_missing` remain local failure states.
- Result consistency in official metrics remains deferred and separately governed by the metrics contract.
