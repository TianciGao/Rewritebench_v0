# Config Discovery Policy

Approved external SQLSolver discovery variables:

- `SQLRB_SQLSOLVER_JAR`
- `SQLRB_SQLSOLVER_ROOT`
- `SQLRB_SQLSOLVER_LD_LIBRARY_PATH`
- `SQLRB_SQLSOLVER_JAVA`

The wrapper discovers the external JAR from `SQLRB_SQLSOLVER_JAR` directly or from `SQLRB_SQLSOLVER_ROOT` by searching build output locations. Java is resolved from `SQLRB_SQLSOLVER_JAVA` or the process `PATH`; the native library path is resolved from `SQLRB_SQLSOLVER_LD_LIBRARY_PATH` or from the external root's `lib/` directory.

The committed source does not hard-code the local SQLSolver root, JAR path, or library path. Machine-local paths appear only in project-control/audit records documenting completed local runs.

The wrapper still retains an explicit command argument and legacy command-style discovery for local developer shims and fail-closed tests. The documented production path for the externally staged SQLSolver JAR is the approved `SQLRB_SQLSOLVER_*` environment-variable contract above.
