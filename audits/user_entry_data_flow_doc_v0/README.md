# User-Entry Data-Flow Documentation Move

This audit records the documentation-only move of the detailed user-entry data-flow and file-location map out of the top-level Chinese `README.md` and into `docs/USER_ENTRY_DATA_FLOW.md`.

Scope:

- Top-level `README.md` simplified to a concise `运行后看哪里` section.
- Detailed user-entry data-flow map created under `docs/USER_ENTRY_DATA_FLOW.md`.
- No source code, scripts, tests, examples, cases, manifests, SQL, schemas, checker files, validation files, case sets, inventory, reports, results, denominator scaffolds, paper results, or raw retained evidence were modified.

Validation summary:

- Documented smoke commands were rerun.
- User-entry tests were rerun.
- Protected-surface diff check confirmed only allowed documentation, audit, and project-control files changed.

Boundary:

- User-entry outputs remain local diagnostics only.
- No official metrics, DB/checker execution, paper tables, reports/results updates, retained evidence creation, or global leaderboard were produced by this task.
