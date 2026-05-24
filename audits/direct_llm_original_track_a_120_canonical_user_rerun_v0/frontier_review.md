# Frontier Review

Non-exact frontier:

```text
mismatch=10
candidate_execution_failed=3
unsupported_engine=5
```

Mismatch rows:

```text
CONS_0005/postgres
PERF_0062/mysql
CONS_0005/mysql
CONS_0037/mysql
PORT_0004/mysql
PORT_0012/mysql
PORT_0013/mysql
PORT_0022/mysql
PORT_0024/mysql
CONS_0005/spark
```

Candidate execution failed:

```text
CONS_0009/spark
CONS_0011/spark
LONGTAIL_0012/spark
```

Unsupported/fail-closed Spark rows:

```text
PORT_0008/spark
PORT_0012/spark
PORT_0022/spark
PORT_0024/spark
PORT_0025/spark
```

Repair-1 should target this frontier only after a separate design/authorization step.
