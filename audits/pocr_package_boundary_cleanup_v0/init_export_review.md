# `__init__.py` Export Review

Reviewed file:

- `src/sql_rewrite_bench/pocr/__init__.py`

Current state:

- `__init__.py` provides broad convenience exports for POCR parser models, Stage A schema/client helpers, annotation resolver helpers, candidate resolver helpers, diagnostic output helpers, Stage B validation helpers, and user facade/output helpers.
- It also exports some earlier scaffold/audit-helper symbols:
  - `DiagnosticPOCRDraftRow`
  - `build_diagnostic_drafts`
  - `diagnostic_draft_fields`
  - `diagnostic_draft_to_csv_rows`
  - `write_diagnostic_draft_csv`
  - `POCRRowDraft`
  - `StaticStageBDiagnosticRow`
  - `build_static_stage_b_diagnostic_rows`
  - `static_stage_b_diagnostic_fields`
  - `static_stage_b_diagnostic_to_csv_rows`
  - `write_static_stage_b_diagnostic_csv`

Decision for this task:

- Do not change exports.
- Do not reduce `__all__`.
- Do not risk import churn before release v0.

Recommendation for future cleanup:

- A separately authorized refactor can narrow public package exports to parser/core/user-facade symbols and move audit helpers under `src/dev` or a `pocr/audit` subpackage.
- That future refactor should include import-compatibility tests and migration notes.

Behavior change in this task: none.
