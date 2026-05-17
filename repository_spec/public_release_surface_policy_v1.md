# Public Release Surface Policy v1

Status: policy

## Purpose

This policy distinguishes the current release construction repository from the final public release surface.

`Rewritebench_v0` is currently a construction and migration work repository. It intentionally contains project-control logs, migration audits, planning previews, future prompts, draft specifications, and intermediate governance artifacts. Those files are useful for safety and traceability, but they are not automatically part of the final public v0 reviewer/user-facing repository.

The final public v0 release should be produced through a clean public export branch or a clean public release repository containing selected files only.

This policy does not delete files, rewrite history, create a release branch, change denominators, change paper results, migrate cases, or update reports/results.

## File Classification Labels

- `PUBLIC_FINAL`: intended to appear in the final public v0 surface.
- `PUBLIC_SUPPORT`: may appear in the final public surface as supporting reference material if curated and public-safe.
- `MAINTAINER_ARCHIVE`: useful for maintainers and traceability, but not intended for the minimal reviewer/user-facing surface.
- `DROP_BEFORE_V0`: construction-only or preview-only material that should not be exported unless explicitly promoted.
- `PRIVATE_ONLY`: must not be published because it may contain sensitive, local, private, prompt, or raw runtime material.

## Likely PUBLIC_FINAL Categories

The clean public surface should normally retain these categories when they exist and pass public hygiene checks:

- `README.md`
- `LICENSE`
- `CITATION.cff`
- `CONTRIBUTING.md`
- `benchmark_spec/`
- final `repository_spec/` policies only
- `taxonomy/`
- `inventory/`
- `case_sets/`
- `cases/`
- public `scripts/`
- public `src/`
- `docs/`
- `tests/`
- public `baselines/`
- curated `reports/evaluation/`
- curated `results/retained/`
- `runs/.gitignore` only, if a top-level local-output placeholder is needed

## Likely PUBLIC_SUPPORT Categories

These categories may be included only when curated and useful to reviewers/users:

- final validator specifications
- final retained-evidence policy documents
- final public runner output policy
- report-renderer documentation
- curated provenance summaries
- curated public retained evidence maps

Drafts should be promoted to final policies before export or moved to maintainer archive.

## Likely MAINTAINER_ARCHIVE Categories

These categories should remain available to maintainers during construction but should not be assumed to belong in the minimal final public surface:

- `audits/`
- `project_control/MIGRATION_RUN_LOG.md`
- intermediate migration reports
- readiness previews
- run-log finalization notes
- draft decision packets after final specs are promoted
- construction-only status snapshots
- one-off planning matrices

## Likely DROP_BEFORE_V0 Categories

These categories are construction scaffolding and should be dropped from the clean public export unless explicitly promoted:

- `future_prompts/`
- temporary planning prompts
- preview-only files
- generated intermediate CSVs not needed by reviewers/users
- task-local audit bundles that duplicate final documentation
- stale draft specs superseded by final policies

## PRIVATE_ONLY Categories

These categories must not enter the clean public surface:

- prompt logs
- chat logs
- Codex or agent control files
- AI workflow rules
- local secrets
- credentials and API keys
- local run outputs
- raw private archives
- raw stdout/stderr logs with private paths
- files with local paths or sensitive traces
- private service endpoint references

## Clean Export Approach

During active redevelopment, do not rewrite history and do not delete construction audits only to make the construction repo look public-ready.

At release time:

1. Classify repository paths using this policy.
2. Choose a clean public branch or a clean public release repository.
3. Export selected files only.
4. Exclude construction scaffolding unless explicitly promoted.
5. Run static case-package validators on exported cases.
6. Run public hygiene scans on exported files.
7. Verify `case_sets/`, inventory, reports, results, and docs agree with the release scope.
8. Tag the release only after clean surface verification passes.

## Branch Versus Separate Repository

Either a clean export branch or a clean public repository may be used.

A clean export branch keeps release state near the construction repository but may still expose construction history unless handled carefully.

A clean public release repository provides a simpler reviewer/user-facing surface when history cleanliness matters.

The default recommendation is to prepare an export manifest first, then choose branch versus repository based on maintainer release requirements.

## Explicit Non-actions

This policy does not:

- delete files now;
- remove audits now;
- remove `project_control/` now;
- rewrite Git history now;
- create a release branch now;
- create a new public repository now;
- migrate cases;
- update reports/results;
- update case sets;
- change denominator values;
- change paper results;
- change case membership;
- modify raw legacy evidence.
