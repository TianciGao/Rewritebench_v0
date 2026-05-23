# Source Hardcoded Path Scan

Scan scope:

- `src/`
- `tests/`
- `scripts/`
- `docs/`
- `repository_spec/`
- `.github/`

SQLSolver-specific machine-local path scan:

- No committed source/test/script/doc/workflow path contains `/home/tianci_gao/.local/share/sqlrb/sqlsolver`.
- No committed source/test/script/doc/workflow path contains `sqlsolver-v1.1.0.jar`.
- No committed source/test/script/doc/workflow path contains a hard-coded `SQLSolver/build/libs` runtime path.

Repository-wide third-party artifact scan excluding audits, runtime output, and `runs/user` found no SQLSolver source tree, SQLSolver JAR, Z3 native libraries, ANTLR libraries, Gradle caches, or SQLSolver build outputs.

Project-control and audit files intentionally record machine-local SQLSolver paths as historical local diagnostic provenance.
