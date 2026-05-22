# Phase 2 Implementation Requirements

This file defines requirements for a future exact-gated local timing diagnostic implementation. It is not an implementation.

## Required Gates

Phase 2 must:

- run timing only after checker exactness is known;
- keep non-exact rows visible as timing-ineligible;
- preserve selected/generated/preflight/execution/checker/exact/timed funnel counts;
- keep label-only mismatch rows timing-ineligible under the current strict-label policy;
- reject unsupported/fail-closed rows from timing while preserving their N.A. status.

## Required Artifact Behavior

Phase 2 must write local timing artifacts only under `runs/user/{run_name}/timing/`.

It must create or reference:

- timing row JSON artifacts with inline sample arrays;
- timing policy artifact;
- timing environment metadata artifact;
- source/candidate SQL hashes;
- result/checker artifact paths where available.

## Required Timing Behavior

Phase 2 must:

- use `warmup_count=1`;
- use `measured_repetitions=5`;
- use `timeout_seconds=30`;
- compute median from complete sample arrays only;
- set `speedup_ratio=null` unless timing is complete, exact-gated, and both medians are positive;
- use `timing_status=partial_failure` for incomplete sample collection;
- record `timing_na_reason` for every untimed, ineligible, failed, timeout, or partial row.

## Required Grouping Behavior

Phase 2 summaries must group by:

- `route_id`;
- `method_id`;
- `engine`;
- `denominator_id`;
- `timing_policy_id`;
- `local_run_id`;
- `candidate_id`.

Combined route aggregates are not allowed unless explicitly diagnostic and non-leaderboard.

## Required PORT/Cross-Engine Behavior

Phase 2 must use resolved manifest role metadata for PORT/cross-engine rows. It must not infer source/reference roles from filenames, SQL text, or directory names.

Cross-engine timing must measure the target-engine source/reference and target candidate in the same target-engine run context.

## Explicit Non-Goals

Phase 2 must not:

- compute official metrics;
- update reports/results;
- render paper tables;
- promote retained evidence;
- create a leaderboard;
- implement POCR;
- create skill folders;
- infer operation atoms;
- change denominators;
- change case membership.
