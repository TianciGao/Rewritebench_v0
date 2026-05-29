# Build Environment

External checkout:

- Path: `/home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver`
- Commit: `dcc2a91d8971a4c4d30b055f99d7d8428a1b754b`
- Git status after build: clean

Java:

```text
openjdk version "17.0.18" 2026-01-20
OpenJDK Runtime Environment (build 17.0.18+8-Ubuntu-124.04.1)
OpenJDK 64-Bit Server VM (build 17.0.18+8-Ubuntu-124.04.1, mixed mode, sharing)
```

Gradle:

- System `gradle`: unavailable.
- Project wrapper: `./gradlew`, Gradle 7.4.
- README mentions Gradle 7.3.3, but the official repository wrapper currently points to Gradle 7.4.

Build:

- Command: `./gradlew fatJar`
- Result: success
- JAR: `/home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver/build/libs/sqlsolver-v1.1.0.jar`

Native libraries:

- `LD_LIBRARY_PATH` for wrapper/smoke: `/home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver/lib`
- Observed libraries: `libz3.so`, `libz3java.so`, `z3-4.13.0.jar`, `antlr-4.8-complete.jar`
