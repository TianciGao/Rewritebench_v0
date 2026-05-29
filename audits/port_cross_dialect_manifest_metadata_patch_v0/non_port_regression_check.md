# Non-PORT Regression Check

## Modified Manifests

Only these PORT manifests were modified:

- `cases/PORT/PORT_0003/manifest.yaml`
- `cases/PORT/PORT_0004/manifest.yaml`
- `cases/PORT/PORT_0005/manifest.yaml`
- `cases/PORT/PORT_0008/manifest.yaml`
- `cases/PORT/PORT_0012/manifest.yaml`
- `cases/PORT/PORT_0013/manifest.yaml`
- `cases/PORT/PORT_0022/manifest.yaml`
- `cases/PORT/PORT_0024/manifest.yaml`
- `cases/PORT/PORT_0025/manifest.yaml`

## Non-PORT Manifests

No PERF, CONS, or LONGTAIL manifests were modified.

## Expected Behavior Boundary

Cases without `local_diagnostic.cross_dialect_reference` continue the default same-engine local diagnostic path until a future runner task consumes explicit metadata.

Representative non-PORT behavior should remain unchanged for:

- `PERF_0006`
- `CONS_0005`
- `LONGTAIL_0011`

## Protected Boundaries

- `case_sets/` unchanged.
- Denominators unchanged.
- Reports/results unchanged.
- Official metrics not computed.
- Timing/speedup not computed.
- No tag score/ranking.
- No leaderboard.
