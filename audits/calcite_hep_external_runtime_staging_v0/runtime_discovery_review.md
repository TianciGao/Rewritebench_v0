# Runtime Discovery Review

The adapter discovery contract is environment-variable based:

- `SQLRB_CALCITE_HEP_CMD`
- `SQLRB_CALCITE_HEP_JAR`
- `SQLRB_CALCITE_HEP_ROOT`
- `SQLRB_CALCITE_HEP_JAVA`
- `SQLRB_CALCITE_HEP_MODE`
- `SQLRB_CALCITE_HEP_TIMEOUT`

Discovery behavior:

- If `SQLRB_CALCITE_HEP_CMD` resolves to an executable command, the adapter treats the runtime as available.
- If no command is configured but `SQLRB_CALCITE_HEP_JAR` exists and Java is available, the adapter uses `java -jar <jar>`.
- If Java is missing, the adapter records `calcite_java_missing`.
- If no command/JAR/root exists, the adapter records `calcite_runtime_unavailable`.
- If partial configuration points to missing paths, the adapter records `calcite_runtime_incomplete`.

No machine-local Calcite path is hard-coded in committed adapter source or tests. The tiny smoke used the staged local command only through environment variables.

Runtime found for this task:

- `SQLRB_CALCITE_HEP_CMD=/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke`
- `SQLRB_CALCITE_HEP_ROOT=/home/tianci_gao/.local/share/sqlrb/calcite_hep`
- `SQLRB_CALCITE_HEP_JAVA=/usr/bin/java`
- `SQLRB_CALCITE_HEP_TIMEOUT=30`
