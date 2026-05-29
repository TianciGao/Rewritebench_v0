# Gap List

## Compatibility Gaps

- Optional PostgreSQL DB/checker diagnostic mode is not compatible with the current normalized case-package layout. It still expects `schema/postgres/ddl.sql` and `schema/postgres/load.sql` under each case package.
- The current executable schema source of truth is external schema packages referenced by manifest `schema.external_profile`; the user-entry DB helper does not use that resolver.
- CLI help exposes optional DB/checker flags, but the public user guide emphasizes a non-DB MVP and does not explain the experimental flags.
- A tiny one-command public smoke still needs polish. The required tiny smoke uses a temporary case-list file, and the current dummy adapter lives under `tests/user_entry/fixtures/`.

## Nonblocking Compatibility Notes

- Non-DB adapter capture is compatible with the current case-package layout.
- Metadata-driven selection still resolves Common-core rows from `case_sets/common_core_v0/`, not by scanning `cases/`.
- All 40 Common-core rows resolve to `sql/source.sql`.
- Output-root restrictions are effective: user outputs stay under `runs/user/<run_id>/` and are local diagnostics only.

## Deferred Release Work

- Full paper reproduction CLI.
- Official metric computation.
- Paper table rendering.
- Retained-evidence adapter / report-output flow.
- Reports/results updates.
- Global leaderboard creation, which remains out of scope by policy.

## Next Safe Action

Run a narrow user-entry repair task focused on external-schema-aware optional DB/checker execution and public smoke command polish. Do not compute metrics or update paper/reporting surfaces in that task.
