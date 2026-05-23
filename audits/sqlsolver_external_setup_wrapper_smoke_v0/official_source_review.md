# Official Source Review

The official SQLSolver README describes SQLSolver as a formal SQL equivalence prover using linear integer arithmetic.

Relevant README facts used by this task:

- Requirements include Java 17 and Gradle.
- The project can be compiled with Gradle and packaged with `gradle fatjar`.
- The JAR is generated under `build/libs/`.
- The JAR CLI shape is `java -jar sqlsolver.jar -sql1=<query1> -sql2=<query2> -schema=<schema> [-print] [-output=<output>]`.
- Each SQL input file stores one SQL statement per line, and corresponding lines are verified as pairs.
- `LD_LIBRARY_PATH` must point to the directory containing `libz3.so` and `libz3java.so`.
- SQLSolver result values are `EQ`, `NEQ`, `UNKNOWN`, and `TIMEOUT`.
- SQLSolver may return `NEQ` or `UNKNOWN` for some equivalent pairs, and timeout behavior can be affected by external libraries such as Z3.

SQL-RewriteBench interpretation:

- SQLSolver is a verifier/support tool, not a rewrite baseline.
- SQLSolver evidence must be shown with coverage and decidability boundaries.
- Local result-checker exactness must not substitute for SQLSolver equivalence.
