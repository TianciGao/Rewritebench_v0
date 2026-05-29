# Environment Requirements

## Current Local Environment

No reusable verifier environment was detected:

- `command -v verieql`: not found.
- `command -v VeriEQL`: not found.
- `command -v sqlsolver`: not found.
- `command -v SQLSolver`: not found.
- `VERIEQL`, `SQLSOLVER`, `JAVA_HOME`, `LD_LIBRARY_PATH`, and `Z3` environment signals: not visible.
- `/tmp/verieql-probe-venv`: absent.
- `/tmp/rewritebench_sqlsolver_audit/candidate`: absent.

## VeriEQL Historical Requirements

Legacy notes suggest VeriEQL reuse would need:

- a staged VeriEQL source tree or installed command,
- Python environment compatible with the tool,
- `z3-solver`,
- a bounded batch entrypoint similar to `python -m parallel.cli_within_timeout`,
- case-to-VeriEQL schema/constraint/pair bridge,
- explicit timeout and constraint policy.

These requirements are historical notes only; they are not satisfied by the current inspected paths.

## SQLSolver Historical Requirements

Legacy notes suggest SQLSolver reuse would need:

- Java 17,
- Gradle if building from source,
- Z3 native/JAR artifacts,
- ANTLR support,
- a built SQLSolver jar or equivalent command,
- a schema file plus paired SQL inputs,
- explicit timeout and unsupported/unknown mapping policy.

These requirements are historical notes only; they are not satisfied by the current inspected paths.

## Recommended Command-Path Policy

Future verifier runs should require explicit tool availability:

```text
SQLRB_VERIEQL_CMD=<external command>
SQLRB_SQLSOLVER_CMD=<external command>
```

or the existing `sqlrb user verify --tool-cmd <path-or-command>` path. Without that, the wrappers should continue to produce local-only `N.A.` / fail-closed verifier summaries.
