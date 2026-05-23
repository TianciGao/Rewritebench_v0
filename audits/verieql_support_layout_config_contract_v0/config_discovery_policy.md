# Config Discovery Policy

Approved external VeriEQL discovery variables:

- `SQLRB_VERIEQL_ROOT`
- `VERIEQL_ROOT`
- `SQLRB_VERIEQL_PYTHON`
- `SQLRB_VERIEQL_CMD`

The wrapper discovers a staged VeriEQL source root from `SQLRB_VERIEQL_ROOT` or `VERIEQL_ROOT`. It validates source-tree shape only and does not install or import dependencies during detection.

This task added support for `SQLRB_VERIEQL_PYTHON` in staged-root batch mode. When a root is supplied and no explicit command is supplied, the wrapper can now build:

`<SQLRB_VERIEQL_PYTHON> -m parallel.cli_within_timeout`

or, for finite-bound mode:

`<SQLRB_VERIEQL_PYTHON> -m parallel.cli_within_bound`

`SQLRB_VERIEQL_CMD` remains the explicit command override. The committed source does not hard-code the local VeriEQL root or Python venv path. Machine-local paths appear only in project-control/audit provenance.
