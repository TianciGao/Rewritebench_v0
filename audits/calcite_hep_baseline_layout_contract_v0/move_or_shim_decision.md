# Move Or Shim Decision

Decision: move the route-specific adapter and leave no compatibility shim.

Reasoning:

- The adapter is a baseline route adapter, not reusable core code.
- D035 explicitly places baseline adapters/routes under `baselines/`.
- The file was introduced in the immediately preceding scaffold task and has no stable public API contract.
- Keeping a source-package shim would preserve route-specific baseline surface under `src/sql_rewrite_bench/`, which is what this task is correcting.

Moved:

- From: `src/sql_rewrite_bench/calcite_hep_fail_closed_adapter.py`
- To: `baselines/calcite_hep_fail_closed/adapter.py`

Shim status:

- No compatibility shim remains under `src/sql_rewrite_bench/`.
- Tests and tiny validation now invoke the baseline adapter path directly.
