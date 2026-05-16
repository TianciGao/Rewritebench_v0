# Public Runner Output Policy v1 Draft

Status: draft

Purpose: define where new user and reproduction outputs should be written in the public workbench.

This draft does not implement runners and does not authorize DB validation, evidence regeneration, timing reruns, metrics computation, or paper table updates.

## Core Policy

Case-local `runs/` is legacy retained evidence. New public runner outputs must not write into case-local `runs/` by default.

New outputs should go to an explicit run output root such as:

- `runs/local/<run_id>/`;
- `reports/user_runs/<run_id>/`;
- `results/local/<run_id>/`.

The final output root is TBD. Public runners must accept an output root argument.

## Case-Local Runs Boundary

Case package `runs/` directories are retained legacy evidence surfaces only. They may be referenced through `evidence/runs_retention.yaml`, but they should not receive new user outputs.

Rules:

- do not append new outputs to case-local `runs/`;
- do not overwrite retained evidence;
- do not delete retained evidence;
- do not mix local user outputs with curated retained evidence.

## Output Root Requirements

Every future public runner should:

- require or derive a run ID;
- accept an output root;
- write a run manifest;
- write machine-readable evidence ledger rows;
- write logs outside case packages;
- record software/environment metadata without exposing secrets;
- avoid absolute local paths in public artifacts;
- avoid prompt, API token, credential, and private endpoint leakage.

## Retained Evidence Immutability

Retained evidence is immutable unless explicitly curated by a bounded retained-evidence migration task.

Adapters may read retained evidence, but should write derived public summaries to approved output roots or retained-evidence target directories, not back into source case packages.

## Validation Scripts Caveat

Validation scripts copied inside migrated case packages are retained legacy validation assets. They are not final public user runners.

Future public runners should be designed against:

- canonical case packages;
- aligned case sets and inventory;
- evidence ledger schema;
- metrics contract;
- output policy.

## Public Hygiene Rules

Public outputs must not include:

- local absolute paths;
- raw stdout/stderr paths by default;
- WSL or host-specific traces;
- credentials;
- API keys;
- prompt/model traces unless explicitly reviewed and sanitized;
- private service endpoints.

## Reports And Results Boundary

Writing user outputs under `reports/user_runs/` or `results/local/` does not imply paper result changes. Paper-facing retained evidence and paper tables require separate approval and validation.

## Open Questions

- Final output root convention.
- Required run manifest fields.
- How user submissions map to `candidate_id`.
- Whether public v0 exposes retained evidence only or also supports fresh user runs.
- Whether LLM baseline reruns are in scope for public v0.
