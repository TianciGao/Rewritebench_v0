# Validation Scope Review

Validation performed in this task:

- Inspected `source.sql`, `pos_01.sql`, `neg_01.sql`, `skills.md`, `manifest.yaml`, checker metadata, and Common-core membership.
- Replaced only `cases/LONGTAIL/LONGTAIL_0011/sql/pos_01.sql`.
- Confirmed corrected `pos_01.sql` contains:
  - `ORDER BY p.Score DESC`
  - `AS PostRank`
  - `MaxRank`
  - `rp.PostRank = mr.MaxPostRank`
- Confirmed corrected `pos_01.sql` no longer contains:
  - `ORDER BY p.Score ASC`
  - `WorstRank`
  - `rp.WorstRank = 1`

DB/checker validation status: deferred.

Reason: the available case validation entrypoint `cases/LONGTAIL/LONGTAIL_0011/validation/run_validation.sh` invokes engine validation through `run_engine_queries.py`. This task allowed a case-local correction and audit, but did not authorize broad DB/checker/timing execution. A later explicitly authorized single-case validation can run:

```bash
cases/LONGTAIL/LONGTAIL_0011/validation/run_validation.sh
```

No baseline rerun, user-run metrics rerun, POCR annotation generation, live API call, broad DB/checker/timing run, paper-facing metric update, denominator change, or case membership change occurred.
