# Audit-Only Helpers Review

The following modules are retained for traceability to prior POCR audit packets. They are not stable public API and are not default user commands.

## `live_smoke.py`

Purpose: bounded live API smoke runner for POCR Stage A annotation.

Reason retained: preserves the implementation path used for earlier 2-4 case live smoke evidence.

Boundary: not used by normal `sqlrb user pocr-diagnostic`; must not be used to promote official metrics.

## `calibration_runner.py`

Purpose: positive-control vs no-op calibration runner, including transformation-aware full-40 calibration.

Reason retained: preserves calibration reproducibility and D037 transformation-aware policy evidence.

Boundary: diagnostic calibration only; not route-level POCR aggregation.

## `real_route_diagnostic_runner.py`

Purpose: one-off Direct LLM original PG40 diagnostic runner over existing candidate SQL.

Reason retained: preserves the audit path that produced the route-bound annotation JSONL later replayed by user-facing diagnostics.

Boundary: internal audit helper; users should use the documented replay path instead.

## `stage_b_static_runner.py`

Purpose: bounded diagnostic runner combining candidates, annotations, and static Stage B checks.

Reason retained: supports prior Stage B static evidence validation packet.

Boundary: static support diagnostics only; no official POCR.

## `draft_runner.py`

Purpose: dry-run diagnostic draft rows from existing candidates and optional annotations.

Reason retained: supports earlier candidate-resolver/draft-runner packet.

Boundary: draft rows only; no route-level score.

## `pocr_row.py`

Purpose: row-level draft model retained from initial POCR interface scaffolding.

Reason retained: compatibility with earlier tests and imports.

Boundary: fixture/draft model only; not paper-facing metric output.

## Shared Boundary

These modules should not write paper-facing reports/results, create leaderboards, compute official Positive Operation Coverage Rate, aggregate route-level POCR, rerun baselines, or modify case packages.
