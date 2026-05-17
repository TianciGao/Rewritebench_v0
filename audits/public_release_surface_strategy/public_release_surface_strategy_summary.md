# Public Release Surface Strategy Summary

Date: 2026-05-17

## Purpose And Scope

This policy task records the maintainer-approved strategy that `Rewritebench_v0` is currently a release construction and migration work repository. The final public v0 release should be produced through a clean export branch or a clean public release repository.

No cleanup was performed. No files were deleted. No history was rewritten. No release branch was created. No cases were migrated. No reports/results, case sets, denominators, paper results, metrics, scripts, source implementation, or raw legacy evidence were changed.

## Why The Strategy Is Needed

The construction repository intentionally contains migration audits, project-control logs, planning previews, future prompts, temporary strategy files, draft specifications, and governance matrices. These artifacts are useful for coordination and review during redevelopment, but they would make the final reviewer/user-facing repository noisy if exported wholesale.

A clean export step lets maintainers preserve construction traceability while publishing a minimal public surface focused on cases, case sets, inventory, benchmark specs, docs, curated reports/results, public scripts, source code, tests, and CI.

## What Remains In The Construction Repo

Current audits, project-control logs, future prompts, draft policy packets, readiness previews, and intermediate CSVs remain in this repository during active redevelopment. They should not be deleted as part of this policy task.

## What Should Be Clean-exported Later

The future clean export should select only public-facing material:

- canonical Common-core case packages;
- approved `case_sets/` and inventory files;
- final benchmark and repository specs;
- user-facing docs and README/license/citation/contribution files;
- public scripts and source implementation;
- curated retained evidence and reports/results;
- tests and CI configuration.

## Why Current Audits Are Scaffolding

Audit bundles and future prompts are construction controls. They document how decisions were reached and keep migration safe, but they are not necessarily useful to a benchmark user or reviewer. They should usually become maintainer archive material or be dropped from the clean public export unless explicitly promoted.

## No Deletion Or History Rewrite

This task records strategy only. It does not delete audits, remove project-control files, rewrite Git history, create an orphan branch, create a clean release branch, or create a new public repository.

## Next Safe Action

Continue redevelopment in the construction repository. Before public v0 release tagging, run a separate clean-export surface classification and pruning task that selects final public files, runs validators and hygiene scans, and then creates a clean export branch or public release repository.
