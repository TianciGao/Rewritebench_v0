# Validator Limitations

This validator checks only synthetic ledger fixtures under `audits/ledger_schema_validation_fixtures/`.

It is not a production retained-evidence adapter and does not validate real retained evidence, legacy reports/results, real case runs, migrated case packages, or paper-facing result tables.

It does not compute metrics, render paper tables, mutate fixtures, write case-local `runs/`, write `reports/`, write `results/`, change denominator values, or change paper results.

Some future production ledger columns named by the policy matrix are not materialized in the current synthetic fixture CSV. The validator reports those as fixture-skeleton warnings rather than hard failures so that the intentionally valid synthetic rows remain usable. A future production ledger validator should fail closed once the materialized production ledger schema is finalized.

Future production ledger validation, retained-evidence parsing, adapter implementation, metrics computation, reproduction CLI work, and paper table rendering require separate authorization.
