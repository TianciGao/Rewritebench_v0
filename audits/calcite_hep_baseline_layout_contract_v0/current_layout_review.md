# Current Layout Review

Before this task:

- Route-specific Calcite adapter file: `src/sql_rewrite_bench/calcite_hep_fail_closed_adapter.py`.
- Focused tests referenced the `src/` path.
- `baselines/` contained only the existing SQLGlot adapter layout.

Assessment:

- The Calcite adapter is route-specific because it defines the `calcite_hep_fail_closed` route identifiers, reads adapter-runner environment variables, emits per-row route status, and intentionally produces no candidate SQL.
- It does not expose reusable SQL-RewriteBench core APIs.
- Keeping it under `src/sql_rewrite_bench/` would blur the D035 boundary between core implementation and baseline route adapters.

After this task:

- Route-specific adapter: `baselines/calcite_hep_fail_closed/adapter.py`.
- Route README: `baselines/calcite_hep_fail_closed/README.md`.
- Core route identity helper remains in `src/sql_rewrite_bench/local_timing.py`.
- No `src/sql_rewrite_bench/calcite_hep_fail_closed_adapter.py` file remains.
