# Migration Timing Recommendation

Do not physically migrate the repository layout now.

## Rationale

- Current case resolution and validators reference `cases/`, `case_sets/`, `schemas/`, and `inventory/`.
- Current tests and development scripts reference existing construction paths.
- Existing audits and project-control records describe current paths and must remain interpretable.
- Moving directories before the output and CLI contracts are designed would create unnecessary churn and risk.

## Recommended Timing

1. Record the target layout as D035.
2. Design the user output contract around `output/results|logs|reports/<run_id>/`.
3. Design the public CLI facade under `src/cli`.
4. Plan resolver/test/validator path abstraction for `benchmarks/`.
5. Run a separate physical layout migration or clean export task only after path compatibility is ready.

## Required Future Validation

A future migration/export task should validate:

- case package resolution;
- Common-core case-set membership;
- schema resolution;
- inventory references;
- user-run output writes;
- CLI entrypoints;
- validators and tests;
- reports/results official-surface boundaries.
