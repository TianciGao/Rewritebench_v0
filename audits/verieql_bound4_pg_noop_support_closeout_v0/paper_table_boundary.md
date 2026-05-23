# Paper Table Boundary

Paper-facing Semantic Equivalence Rate remains blocked.

Reasons:

- Only 4 of 35 exact rows pass identity sanity.
- 31 exact rows fail the identity guard.
- Corrected decidable coverage is 4/35.
- Unsupported, timeout, not-implemented, and tool-error rows dominate the ledger.
- `LONGTAIL_0023` demonstrated that identity guard is necessary because the tool can return non-equivalent for identity pairs on at least one supported-looking SQL shape.

Required statement:

- The corrected local diagnostic SER is not official Semantic Equivalence Rate.
- It is not paper evidence.
- It must not be promoted into paper tables, top-level `reports/`, top-level `results/`, or retained evidence.

Full Common-core or full baseline SER must not be claimed from VeriEQL in the current state.
