# CONS_0007 Future Canary Plan

## Status

`CONS_0007` is recorded as the future first bounded VeriEQL support candidate. It was not executed in this task.

## Why CONS_0007

Legacy readiness classified `CONS_0007` as the only first `support_candidate`.

Reasons:

- compact Calcite-derived consistency case
- source/positive/negative SQL shape available in legacy case package
- schema material available
- useful source-positive and source-negative support pairs

## Caveat

Legacy historical VeriEQL JSONL output outside `baseline_smoke` showed `Not supported feature: EXISTS` for `CONS_0007`. That means it is a good compatibility canary, not a guaranteed equivalence proof candidate.

## Future Run Conditions

A real `CONS_0007` VeriEQL canary should require:

- explicit `SQLRB_VERIEQL_ROOT`
- dependencies installed outside this task
- bounded pair scope only
- D035 output placement
- raw stdout/stderr retention
- local-only boundary flags
- no Common-core/full CONS run
- no official Semantic Equivalence Rate

## This Task

This task ran only a temp-root dry-run JSONL construction smoke using `CONS_0007` metadata. The command was not executed.
