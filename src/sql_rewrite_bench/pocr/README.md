# POCR Package Boundary

## Purpose

This package implements optional Positive Operation Coverage diagnostic support for SQL-RewriteBench.

It parses case-local root-level `skills.md` contracts, supports Stage A candidate annotation, applies conservative Stage B evidence validation, and writes optional D035-style user diagnostic outputs.

This is not official POCR.

No route-level POCR score is emitted.

No paper-facing metric is promoted.

## Public Entry Points

Normal users should enter through:

```bash
sqlrb user pocr-diagnostic
```

The public and user-facing entry points are:

- `src/cli/pocr_diagnostic.py`: default-off CLI wrapper for `sqlrb user pocr-diagnostic`.
- `src/sql_rewrite_bench/pocr/user_facade.py`: stable internal facade used by the CLI.
- `src/sql_rewrite_bench/pocr/user_output_adapter.py`: D035-style diagnostic output writer.
- `src/sql_rewrite_bench/pocr/diagnostic_output_schema.py`: row, summary, CSV, and Markdown diagnostic output schema.

The command is optional and default-off. It does not run live API calls in annotation-missing or replay mode, does not run DB/checker/timing, does not rerun baselines, and does not compute official metrics.

## Stable Internal Core

The stable internal core is:

- `models.py`: dataclasses for parsed skill contracts and validation issues.
- `skills_parser.py`: root-level `skills.md` parser.
- `validation.py`: contract validation against case directory metadata and required sections.
- `inventory.py`: Common-core inventory scanning and parse-only audit report helpers.
- `candidate_resolver.py`: read-only candidate SQL resolver for existing route-labeled candidate roots.

These modules are implementation internals, but they are the intended foundation for current POCR diagnostic behavior.

## Stage A Annotation Layer

The Stage A annotation layer is:

- `annotation_schema.py`: strict candidate-level annotation schema and validators.
- `prompt_builder.py`: deterministic prompt construction from `skills.md`, source SQL, candidate SQL, and optional control SQL.
- `annotation_client.py`: fake/offline and fail-closed live-client interfaces.
- `json_output_guard.py`: deterministic JSON parse guard for provider responses.
- `annotation_resolver.py`: read-only annotation JSONL replay resolver.

Stage A annotation alone is not counted.

Stage A output is a structured claim source only. It must be checked by Stage B before any diagnostic operation support count is reported.

## Stage B Evidence Layer

The Stage B evidence layer is:

- `evidence_validation.py`: early schema and synthetic-evidence validation interface.
- `static_evidence.py`: explicit static evidence reference checks.
- `transformation_evidence.py`: conservative SQL normalization and source/candidate comparison helpers.
- `operation_evidence_policy.py`: transformation-aware operation evidence policy.

Stage B transformation-aware validation is diagnostic only.

Operation support must be transformation-aware and relative to source. `candidate_sql_span`, `source_sql_span`, and `positive_sql_span` alone are presence or comparison evidence, not operation coverage evidence.

Semantic guard atoms are not part of operation coverage numerator.

## User Diagnostic Output Layer

The user diagnostic output layer is:

- `diagnostic_output_schema.py`: diagnostic row and pool-summary schema.
- `user_output_adapter.py`: writes user-output files under a caller-provided output root.
- `user_facade.py`: thin facade that combines candidates, optional annotation JSONL, Stage B diagnostics, and output writing.

When invoked, outputs go only to D035-style user output paths:

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

Generated output is local user-run output and should not be committed unless a separate task explicitly authorizes promotion.

## Internal Audit / Calibration Helpers

The following modules are internal audit helpers, not stable public API:

- `draft_runner.py`
- `pocr_row.py`
- `stage_b_static_runner.py`
- `live_smoke.py`
- `calibration_runner.py`
- `real_route_diagnostic_runner.py`

These modules reproduce or support prior audit packets. They are not default user commands. They must not be used to promote official metrics. They should not write paper-facing reports/results.

They remain in place for release-v0 traceability and to avoid import churn before release-critical paths are stable.

## Boundary and Non-Goals

This is not official POCR.

No route-level POCR score is emitted.

No paper-facing metric is promoted.

Stage A annotation alone is not counted.

Stage B transformation-aware validation is diagnostic only.

Semantic guard atoms are not part of operation coverage numerator.

No global leaderboard is produced.

This package must not infer operation atoms from taxonomy tags, SQL shape, positive SQL, source SQL, candidate SQL, retained evidence, or ad hoc analysis. Operation atoms come from case-local root-level `skills.md` only.

## Future Cleanup Note

A future larger refactor may move audit helpers under `src/dev` or a `pocr/audit` subpackage.

That refactor is not performed now to avoid import churn before release v0. This task only documents boundaries.
