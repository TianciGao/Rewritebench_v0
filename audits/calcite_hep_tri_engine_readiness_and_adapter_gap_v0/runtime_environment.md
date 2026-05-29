# Runtime Environment

External Calcite runtime:

`/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke`

Environment used for the smoke:

```text
SQLRB_CALCITE_HEP_CMD=/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke
SQLRB_CALCITE_HEP_ROOT=/home/tianci_gao/.local/share/sqlrb/calcite_hep
SQLRB_CALCITE_HEP_TIMEOUT=30
```

Preflight confirmed:

- PostgreSQL local execution environment available.
- MySQL local execution environment available.
- Spark local execution environment available.
- Java available through `/usr/bin/java`.
- External Calcite runtime executable present.

Runtime artifacts were written under:

`/tmp/sqlrb_calcite_hep_tri_engine_readiness_and_adapter_gap_v0/`

D035 export shape was used under the temp root:

- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

No runtime artifacts were staged or committed.
