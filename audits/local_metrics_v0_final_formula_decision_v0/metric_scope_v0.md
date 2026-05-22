# Metric Scope v0

The first non-official local metrics calculator v0 may implement local diagnostic summaries for:

- Coverage
- Result Consistency
- Performance over exact + timed rows

The calculator must preserve grouping by:

- route
- method
- engine
- denominator
- timing policy
- local run
- candidate identity where available

It must keep these statuses visible as diagnostics:

- selected
- candidate generated
- preflight passed
- source executable
- candidate executable
- checker attempted
- exact
- mismatch
- label-only mismatch
- unsupported/fail-closed
- timing eligible
- timed
- timing N.A. reason
- failure bucket

The calculator is not a retained-evidence adapter and is not a paper table renderer.
