# Package Validation Summary Schema Guard Report

## Purpose

This report defines the boundary between case-local validation summaries and task-level construction/audit records. It accompanies `repository_spec/package_validation_summary_schema_v1.md`.

## Why Task Fields Do Not Belong In Case-local Summaries

`evidence/package_validation_summary.json` should summarize intrinsic package validation state: layout, static validation, public hygiene, retained-evidence index presence, checker/config/schema assets, and local caveats. Repository-wide fields such as denominator changes, paper-result changes, reports/results changes, raw legacy evidence changes, commits, pushes, and batch names describe task execution and belong outside the case package.

Mixing task fields into case-local summaries makes public package contents look like they carry repository mutation claims. It also forces future public users to distinguish package facts from construction history, which weakens the package boundary.

## Where Those Fields Should Live

- Task-level mutation boundaries belong in `audits/<task>/` outputs.
- Chronological execution history belongs in `project_control/MIGRATION_RUN_LOG.md`.
- Current high-level state belongs in `project_control/MIGRATION_STATUS.md`.
- Long-term policy belongs in `repository_spec/` or `project_control/DECISION_LOG.md` when a true persistent decision is made.

## Current Audit Result

Package validation summaries audited: 42.

Files needing future normalization under the schema guard: 42.

No package validation summary files were modified by this task.

## Wave 002 Generation Guidance

Future wave 002 package generation should create `evidence/package_validation_summary.json` files that follow `repository_spec/package_validation_summary_schema_v1.md`. Repository-wide boundaries should be recorded in the wave audit outputs and project-control files, not copied into case-local JSON.

## Future Normalization

Existing files may be normalized later by a separate bounded task. That future task should rewrite only case-local summary structure and should not alter evidence, `case_sets/`, reports/results, denominators, paper results, metrics, or raw legacy evidence.
