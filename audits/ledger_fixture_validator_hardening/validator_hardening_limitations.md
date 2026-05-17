# Validator Hardening Limitations

This validator remains fixture-only. It reads synthetic fixture CSVs and static Common-core denominator scaffold files only.

It is not a production retained-evidence adapter, does not validate real retained evidence, and does not parse legacy reports, results, runs, case-local evidence, or raw legacy archives.

It does not compute metrics, render paper tables, validate public reports/results, create production ledger files, write case-local `runs/`, mutate denominator values, or change paper results.

The current synthetic fixture table intentionally omits some future production path columns named by the policy matrix. The validator reports those absent fixture-only columns as warnings so that synthetic fixtures can remain compact. A future production ledger validator should fail closed once the materialized production schema is authorized.

Production ledger validation, retained-evidence adapter implementation, metrics computation, reproduction CLI implementation, public runner implementation, and paper table rendering require separate authorization.
