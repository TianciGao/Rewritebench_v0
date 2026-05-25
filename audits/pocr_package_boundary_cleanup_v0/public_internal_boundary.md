# Public / Internal Boundary

## Public CLI Entry

The public user-facing entry is:

```bash
sqlrb user pocr-diagnostic
```

It is implemented by `src/cli/pocr_diagnostic.py` and remains optional/default-off. Normal users should not invoke internal POCR modules directly.

## Stable Internal Facade

The stable internal facade is:

- `src/sql_rewrite_bench/pocr/user_facade.py`
- `src/sql_rewrite_bench/pocr/user_output_adapter.py`
- `src/sql_rewrite_bench/pocr/diagnostic_output_schema.py`

These modules back the default-off CLI path and write D035-style diagnostic output under caller-provided output roots.

## Stable Internal Core

The stable core modules are:

- `models.py`
- `skills_parser.py`
- `validation.py`
- `inventory.py`
- `candidate_resolver.py`

These modules parse root-level `skills.md`, validate the contract, scan Common-core membership, and resolve existing candidate SQL artifacts read-only.

## Stage A and Stage B Internals

Stage A modules construct or validate structured annotations. Stage A annotation alone is not counted.

Stage B modules validate diagnostic operation support conservatively. Stage B transformation-aware validation is diagnostic only.

Operation support must remain transformation-aware and relative to source. Semantic guard atoms are not part of operation coverage numerator.

## Audit-Only Helpers

The following modules are internal audit helpers:

- `draft_runner.py`
- `pocr_row.py`
- `stage_b_static_runner.py`
- `live_smoke.py`
- `calibration_runner.py`
- `real_route_diagnostic_runner.py`

They remain for traceability to previous audit packets. They are not default user commands and are not stable public API.

## Behavior Change

No behavior changed in this task.

No files were moved. No modules were renamed. No imports were changed. No CLI behavior changed. No official Positive Operation Coverage Rate computation or route-level POCR aggregation was added.
