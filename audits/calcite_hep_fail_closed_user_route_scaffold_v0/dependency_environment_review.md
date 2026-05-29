# Dependency Environment Review

Java status:

```text
openjdk version "17.0.18" 2026-01-20
OpenJDK Runtime Environment (build 17.0.18+8-Ubuntu-124.04.1)
OpenJDK 64-Bit Server VM (build 17.0.18+8-Ubuntu-124.04.1, mixed mode, sharing)
/usr/bin/java
```

Calcite-specific configuration:

- `SQLRB_CALCITE_HEP_CMD`: not configured
- `SQLRB_CALCITE_HEP_JAR`: not configured
- `SQLRB_CALCITE_HEP_ROOT`: not configured
- `SQLRB_CALCITE_HEP_JAVA`: not configured

Result:

- Calcite HEP runtime is not available through the approved environment-variable discovery path.
- The route therefore fails closed with `preflight_status=calcite_runtime_unavailable`.
- No dependency was installed.
- No Calcite source, JAR, native library, Gradle cache, or build output was copied into the release repo.
