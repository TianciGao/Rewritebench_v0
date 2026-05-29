# SQLSolver External Install Review

SQLSolver was cloned and built outside the release repository.

- External path: `/home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver`
- Official source: `https://github.com/SJTU-IPADS/SQLSolver`
- Commit: `dcc2a91d8971a4c4d30b055f99d7d8428a1b754b`
- Build command: `./gradlew fatJar`
- Build result: success
- JAR path: `/home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver/build/libs/sqlsolver-v1.1.0.jar`
- Required native library path: `/home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver/lib`
- Bundled external libraries observed: `libz3.so`, `libz3java.so`, `z3-4.13.0.jar`, `antlr-4.8-complete.jar`
- External source tree status after build: clean

No SQLSolver source, JAR, native library, ANTLR library, Gradle cache, or build output was copied into or committed in the release repository.
