# SQLSolver Candidate Paths

## Search Result

No usable SQLSolver command path was found.

The legacy checkout contains SQLSolver notes but no `.jar`, no checked-in SQLSolver source tree, no executable wrapper, and no local command on PATH.

## Historical Path Mentions

The docs mention an older temporary acquisition/build path:

```text
/tmp/rewritebench_sqlsolver_audit/candidate
```

They also mention a built jar from that temporary path:

```text
/tmp/rewritebench_sqlsolver_audit/candidate/build/libs/sqlsolver-v1.1.0.jar
```

Both paths are absent now.

## Historical Substrate Notes

The legacy notes record:

- Upstream candidate: `SJTU-IPADS/SQLSolver`
- License visible in the upstream audit: Apache License 2.0
- Expected Java entrypoint: `sqlsolver.api.Entry`
- Expected command shape: Java with `-sql1`, `-sql2`, `-schema`, optional `-output`
- Historical dependency notes: Java 17, Gradle, Z3, ANTLR, Python 3
- Historical bounded support smoke over `CONS_0007` / `CONS_0035`

These notes are not a current runnable installation.

## Candidate Command

No current candidate command is available for:

```text
SQLRB_SQLSOLVER_CMD
```

## Interpretation

The release wrapper should continue failing closed unless the user provides an explicit external command path through `--tool-cmd` or a future environment variable. Do not copy historical source trees, jars, `/tmp` build outputs, or support-smoke artifacts into the release repo.
