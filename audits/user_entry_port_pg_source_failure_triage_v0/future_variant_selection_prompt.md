# Future Variant Selection Prompt

Task title:
Design engine-aware source SQL selection for user-entry PostgreSQL PORT diagnostics

Purpose:
Design a narrow local-diagnostic policy for selecting engine-compatible source SQL before PostgreSQL execution. The current runner executes `cases/{POOL}/{CASE_ID}/sql/source.sql` directly. For several PORT cases, `source.sql` is retained MySQL-like SQL while `pos_01.sql` appears PostgreSQL-like but is not declared as a PostgreSQL source oracle.

Scope:

- Design only unless explicitly authorized otherwise.
- Do not edit case SQL.
- Do not edit manifests unless a separate maintainer-approved metadata task authorizes it.
- Do not compute official metrics.
- Do not compute timing/speedup.
- Do not update reports/results.
- Do not create a leaderboard.

Questions to answer:

- Which manifest field should declare an engine-compatible source oracle for local DB diagnostics?
- Can an existing positive rewrite ever serve as an engine-specific source oracle, or must a separate role/path be declared?
- What should the runner do when no approved engine-compatible source SQL exists?
- How should ledger fields distinguish dialect-incompatible source SQL from schema/setup failures?
- How should this remain local diagnostic only and not affect official metrics or paper results?

Expected outputs:

- A design packet under `audits/user_entry_engine_aware_source_selection_design_v0/`.
- A proposed manifest metadata contract or runner-only fail-closed behavior.
- A protected-surface check confirming no case SQL, case_sets, reports/results, denominator, paper results, or raw retained evidence changed.
