# Timing Boundary

## Current State

Timing is not implemented in the user-entry local diagnostic path. U7 does not change that.

## Future Ownership

Engine-specific execution modules may collect raw timing samples later only when explicitly authorized. A future `timing_diagnostic.py` or equivalent timing layer should own interpretation of those raw samples.

## Exact-Only Interpretation

Any future timing interpretation must be exact-only:

- candidate must be generated
- candidate must pass preflight
- source and candidate must execute
- local checker must report exact or the approved correctness basis must be satisfied
- raw timing must be present and eligible

## Deferred Official Metrics

Speedup calculation belongs to a future timing/performance report layer after exactness is known. Official timing metrics require separate authorization and are governed by `repository_spec/metrics_contract_v1.md`.

Deferred metrics include:

- `GM_Speedup`
- `Speedup Ratio Percentiles`
- `SpeedupTransferRate`
- any paper-facing timing table

## U7 Prohibitions

U7 must not:

- collect timing samples
- compute speedup
- compute official metrics
- render paper tables
- update reports/results
- create a leaderboard
