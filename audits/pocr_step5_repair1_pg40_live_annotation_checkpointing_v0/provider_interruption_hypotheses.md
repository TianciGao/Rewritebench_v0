# Provider Interruption Hypotheses

The prior packet does not prove a provider-side error. The safe interpretation is narrower: the orchestration was not checkpointed, so subprocess termination erased useful row-level state.

Plausible causes include:

- provider latency or a response taking longer than expected;
- Python subprocess termination before buffered output or files were flushed;
- missing per-row `pending` manifest writes before the network call;
- no safe partial JSONL write after each completed row;
- no resumable checkpoint state for retrying only incomplete rows.

The new runner addresses these orchestration risks without changing POCR metric boundaries and without running a full PG40 annotation pass.
