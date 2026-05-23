# Non-Timed Frontier

Twenty selected PostgreSQL rows were not timed because they were not exact/result-consistent in the source execution/checker audit.

No-candidate rows:

- `PORT_0003`
- `PORT_0004`
- `PORT_0005`
- `PORT_0008`
- `PORT_0012`
- `PORT_0022`
- `PORT_0025`

Mismatch rows:

- `PERF_0035`
- `PERF_0062`
- `CONS_0011`

Source execution failed rows:

- `PORT_0013`
- `PORT_0024`

Candidate execution failed rows:

- `CONS_0036`
- `CONS_0037`
- `LONGTAIL_0011`
- `LONGTAIL_0012`
- `LONGTAIL_0013`
- `LONGTAIL_0022`
- `LONGTAIL_0023`
- `LONGTAIL_0024`

The 4 schema-fallback rows from the execution/checker audit remain non-timed because none reached exact/result-consistent status.
