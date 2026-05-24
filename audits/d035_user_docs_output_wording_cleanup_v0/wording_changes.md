# Wording Changes

Changed wording to consistently state:

- User-facing output is exported under:
  - `output/results/<run_id>/`
  - `output/logs/<run_id>/`
  - `output/reports/<run_id>/`
- `runs/user/<run_id>/` is internal transitional staging used by the current implementation before export.
- Top-level `reports/` and top-level `results/` are official/paper/release surfaces and require separate authorization.
- Route-specific baseline adapters belong under `baselines/`.
- Core reusable implementation belongs under `src/sql_rewrite_bench/`.
- Public CLI/facade belongs under `src/cli/`.
- Current `cases/`, `case_sets/`, `schemas/`, and `inventory/` paths remain valid until a separate physical migration task.
- `benchmarks/` is the final D035 public target, not the current physical layout.

Files with narrowed wording updates:

- `README.md`
- `docs/README.md`
- `docs/RUN_ARTIFACT_POLICY.md`
- `docs/USER_ENTRY_DATA_FLOW.md`
- `docs/USER_BENCHMARK_GUIDE.md`
- `docs/LOCAL_ENGINE_SETUP.md`
- `baselines/sqlglot/README.md`

No source code or tests were changed.
