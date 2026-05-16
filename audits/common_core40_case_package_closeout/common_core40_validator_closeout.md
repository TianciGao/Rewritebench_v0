# Common-core 40 Validator Closeout

Date: 2026-05-16

## Full-Case Validator

Command:

```bash
python scripts/dev/validate_case_package.py --mode full-case --case cases/PERF/PERF_0006 --case cases/PERF/PERF_0007 --case cases/PERF/PERF_0008 --case cases/PERF/PERF_0013 --case cases/PERF/PERF_0017 --case cases/PERF/PERF_0019 --case cases/PERF/PERF_0024 --case cases/PERF/PERF_0033 --case cases/PERF/PERF_0034 --case cases/PERF/PERF_0035 --case cases/PERF/PERF_0052 --case cases/PERF/PERF_0054 --case cases/PERF/PERF_0056 --case cases/PERF/PERF_0062 --case cases/PERF/PERF_0077 --case cases/PERF/PERF_0082 --case cases/CONS/CONS_0005 --case cases/CONS/CONS_0007 --case cases/CONS/CONS_0009 --case cases/CONS/CONS_0010 --case cases/CONS/CONS_0011 --case cases/CONS/CONS_0012 --case cases/CONS/CONS_0024 --case cases/CONS/CONS_0036 --case cases/CONS/CONS_0037 --case cases/PORT/PORT_0003 --case cases/PORT/PORT_0004 --case cases/PORT/PORT_0005 --case cases/PORT/PORT_0008 --case cases/PORT/PORT_0012 --case cases/PORT/PORT_0013 --case cases/PORT/PORT_0022 --case cases/PORT/PORT_0024 --case cases/PORT/PORT_0025 --case cases/LONGTAIL/LONGTAIL_0011 --out audits/common_core40_case_package_closeout/common_core40_full_case_validator_results.csv
```

Result: PASS 35/35.

Failures: none.

Warnings: none.

## Canonical-Case Validator

Command:

```bash
python scripts/dev/validate_case_package.py --mode canonical-case --case cases/PERF/PERF_0006 --case cases/PERF/PERF_0007 --case cases/PERF/PERF_0008 --case cases/PERF/PERF_0013 --case cases/PERF/PERF_0017 --case cases/PERF/PERF_0019 --case cases/PERF/PERF_0024 --case cases/PERF/PERF_0033 --case cases/PERF/PERF_0034 --case cases/PERF/PERF_0035 --case cases/PERF/PERF_0052 --case cases/PERF/PERF_0054 --case cases/PERF/PERF_0056 --case cases/PERF/PERF_0062 --case cases/PERF/PERF_0077 --case cases/PERF/PERF_0082 --case cases/CONS/CONS_0005 --case cases/CONS/CONS_0007 --case cases/CONS/CONS_0009 --case cases/CONS/CONS_0010 --case cases/CONS/CONS_0011 --case cases/CONS/CONS_0012 --case cases/CONS/CONS_0024 --case cases/CONS/CONS_0036 --case cases/CONS/CONS_0037 --case cases/PORT/PORT_0003 --case cases/PORT/PORT_0004 --case cases/PORT/PORT_0005 --case cases/PORT/PORT_0008 --case cases/PORT/PORT_0012 --case cases/PORT/PORT_0013 --case cases/PORT/PORT_0022 --case cases/PORT/PORT_0024 --case cases/PORT/PORT_0025 --case cases/LONGTAIL/LONGTAIL_0011 --out audits/common_core40_case_package_closeout/common_core40_canonical_case_validator_results.csv
```

Result: PASS 35/35.

Failures: none.

Warnings: `PORT_0004` and `PORT_0008` use the accepted transitional alias `validation/run_pg_validation.sh` for PostgreSQL validation.

## PORT_0004 Status

`PORT_0004` was previously a legacy-compatible full-case pilot and was intentionally excluded from canonical-case regression. After the PORT final bounded batch, it has been upgraded to canonical layout and now passes validator v0.3 canonical-case mode.

## Excluded Cases

`LONGTAIL_0012`, `LONGTAIL_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024` were excluded because they are not yet migrated into canonical release case packages. Excluding them preserves the distinction between fixed Common-core membership and current case-package migration status.
