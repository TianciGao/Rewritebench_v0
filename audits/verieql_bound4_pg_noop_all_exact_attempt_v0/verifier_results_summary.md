# Verifier Results Summary

Outcome counts across all selected rows:

- `equivalent`: 4
- `non_equivalent`: 1
- `timeout`: 8
- `unsupported`: 16
- `not_implemented`: 5
- `syntax_error`: 0
- `unknown`: 0
- `out_of_memory`: 0
- `tool_error`: 1
- `not_attempted`: 5

Decidable rows:

- `CONS_0036`: `equivalent`
- `CONS_0037`: `equivalent`
- `PORT_0003`: `equivalent`
- `PORT_0005`: `equivalent`
- `LONGTAIL_0023`: `non_equivalent`

Timeout rows:

- `PERF_0006`
- `PERF_0008`
- `PERF_0033`
- `PERF_0034`
- `PERF_0054`
- `PERF_0062`
- `LONGTAIL_0022`
- `LONGTAIL_0024`

Unsupported rows:

- `PERF_0007`
- `PERF_0013`
- `PERF_0017`
- `PERF_0035`
- `PERF_0052`
- `PERF_0056`
- `CONS_0005`
- `CONS_0007`
- `CONS_0009`
- `CONS_0010`
- `CONS_0011`
- `CONS_0012`
- `CONS_0024`
- `LONGTAIL_0011`
- `LONGTAIL_0012`
- `LONGTAIL_0013`

Not-implemented rows:

- `PERF_0019`
- `PERF_0024`
- `PERF_0077`
- `PERF_0082`
- `PORT_0008`

Tool-error row:

- `PORT_0012`

The `LONGTAIL_0023` non-equivalent result requires investigation before any promotion because this was a SQLGlot-noop source-vs-candidate row.
