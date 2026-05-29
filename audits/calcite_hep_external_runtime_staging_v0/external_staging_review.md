# External Staging Review

External source/provenance:

- Legacy Calcite source root inspected: `/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/calcite/calcite`
- Git top-level for that tree: `/home/tianci_gao/code/sql-rewrite-bench`
- Legacy repository commit observed: `dd8d2c761e1630a8bcf733be08fc636371bafb0a`
- Legacy repository status was already dirty with unrelated report/workspace changes and was not staged into the release repo.

External build/staging path:

- `/home/tianci_gao/.local/share/sqlrb/calcite_hep/`

Staging commands:

```bash
GRADLE_USER_HOME=/home/tianci_gao/.local/share/sqlrb/calcite_hep/gradle_home \
  ./gradlew --no-daemon :core:classes

javac -cp <external Calcite classes and Gradle-cache jars> \
  -d /home/tianci_gao/.local/share/sqlrb/calcite_hep/classes \
  /home/tianci_gao/.local/share/sqlrb/calcite_hep/src/CalciteHepRewriteSmoke.java
```

The first external invocation probe exposed a missing `org.joou.UShort` runtime dependency. Running the Calcite Gradle wrapper with an external Gradle home materialized `org.jooq:joou-java-6:0.9.5` outside the release repo. The runtime command then succeeded for `PERF_0006`.

Committed artifact policy:

- Calcite source committed: no.
- Calcite JAR/class files committed: no.
- Gradle cache/build output committed: no.
- External staging files remain outside the release repo.
