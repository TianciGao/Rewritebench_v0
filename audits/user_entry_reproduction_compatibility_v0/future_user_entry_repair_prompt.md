# Future User-Entry Repair Prompt

Task title:
Repair user-entry external-schema compatibility and public smoke command

Purpose:
Update the optional user-entry DB/checker diagnostic mode so it works with normalized Common-core case packages and external schema profiles, while preserving the current non-DB adapter-capture path.

Scope:

- Modify `src/sql_rewrite_bench/postgres_execution.py` and related user-entry tests only as needed.
- Resolve executable schema files from case manifest `schema.external_profile` or the v2 resolver, not from case-local `schema/postgres/`.
- Keep all DB/checker outputs under `runs/user/<run_id>/`.
- Keep DB/checker mode local diagnostic only.
- Add or update tests proving DB/checker mode fails closed when external schema metadata is missing and resolves external schema paths when present.
- Add a public smoke convenience: either a public smoke case-list/adapter under an examples namespace or a bounded `--smoke` / `--limit` option.
- Update docs only after implementation behavior is aligned.

Boundaries:

- Do not compute official metrics.
- Do not render paper tables.
- Do not update reports/results.
- Do not modify case packages, manifests, SQL, schemas, checker files, validation files, case sets, inventory, denominator scaffolds, paper results, or raw retained evidence unless explicitly authorized.
- Do not create a global leaderboard.
- Do not claim paper reproduction is complete.

Validation:

- Module and wrapper help.
- Non-DB dry-run and adapter-capture smoke.
- Optional PostgreSQL DB/checker dry/fail-closed tests.
- User-entry unit tests.
- Protected-surface diff checks.
