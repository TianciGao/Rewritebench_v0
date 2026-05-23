# Command Shape Review

The wrapper builds the official SQLSolver JAR command:

```text
java -jar <sqlsolver.jar> -sql1=<sql1_file> -sql2=<sql2_file> -schema=<schema_file> -output=<output_file>
```

Environment variables:

- `SQLRB_SQLSOLVER_JAR`: explicit external JAR path.
- `SQLRB_SQLSOLVER_ROOT`: external SQLSolver root; wrapper searches `build/libs/*.jar`.
- `SQLRB_SQLSOLVER_LD_LIBRARY_PATH`: native library path for Z3.
- `SQLRB_SQLSOLVER_JAVA`: Java executable or command.

Runtime input handling:

- SQL files and schema files generated for SQLSolver invocation are temporary.
- Repository case files are read but not modified.
- Repository-level `output/`, `runs/user/`, top-level `reports/`, and top-level `results/` are not used by the synthetic smoke.

Identity guard planning hook:

- The wrapper can be called for `source-vs-source`, `candidate-vs-candidate`, and `source-vs-candidate` pair records in a future exact-candidate pass.
- A future SER pass must exclude rows from `V_equiv` and `V_non` if identity sanity fails.
