# Misplaced File Review

Tracked baseline-specific files:

- SQLGlot adapter files are under `baselines/sqlglot/`.
- Calcite HEP fail-closed adapter files are under `baselines/calcite_hep_fail_closed/`.
- No tracked route-specific Calcite or SQLGlot adapter file remains under `src/sql_rewrite_bench/`.

Tracked core files:

- `src/sql_rewrite_bench/adapter_runner.py` is reusable runner infrastructure, not a route-specific baseline adapter.
- `src/sql_rewrite_bench/local_timing.py` contains route-identity detection for known adapters. This is shared grouping logic for diagnostics, not a baseline implementation file.
- verifier wrappers under `src/sql_rewrite_bench/verifier_support/` are verifier-support infrastructure, not rewrite baselines.

No tracked file requires a move in this task.

Observed local generated cache note:

- Local `__pycache__` directories may exist in the working tree after Python validation. They are ignored and not tracked; they are not release files and were not staged.

Verdict:

- No tracked user-related file is misplaced enough to justify an optional move in this task.
- No physical migration was performed.
