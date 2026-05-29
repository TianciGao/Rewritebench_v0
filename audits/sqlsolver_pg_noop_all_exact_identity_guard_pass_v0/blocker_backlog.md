# Blocker Backlog

Main SQLSolver blockers in this pass:

- `UNKNOWN` identity behavior on eight exact rows.
- `TIMEOUT` identity behavior on three exact rows.
- Five source-run ineligible PORT rows remained not attempted because they were not exact/result-consistent.

Identity-failed unknown rows:

- `PERF_0035`
- `PERF_0052`
- `PORT_0003`
- `PORT_0005`
- `PORT_0008`
- `PORT_0012`
- `LONGTAIL_0011`
- `LONGTAIL_0013`

Identity-failed timeout rows:

- `PERF_0034`
- `PERF_0062`
- `LONGTAIL_0024`

Next engineering options:

- triage representative `UNKNOWN` rows to determine whether SQLSolver input simplification, schema handling, or tool limits are responsible;
- triage representative timeout rows with a bounded timeout policy probe;
- prepare a separate policy packet for whether a bounded SQLSolver support row can be reported with explicit coverage.
