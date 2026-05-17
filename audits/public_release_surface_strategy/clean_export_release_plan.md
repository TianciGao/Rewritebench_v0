# Clean Export Release Plan

Date: 2026-05-17

## When To Run Clean Export

Run clean export only after the public v0 surface is functionally ready:

- Common-core case packages are final and validator-passing.
- Case sets and inventory are approved.
- Public docs, README, license, citation, and contribution files are ready.
- Curated reports/results or retained evidence surfaces are approved.
- Public scripts/source/tests/CI are implemented or explicitly deferred.
- Public hygiene scans pass.

Do not run clean export during active policy or planning tasks.

## Branch Option

A clean export branch can be created from selected files in the construction repository.

Pros:

- Keeps release artifact near construction history.
- Simple to push and tag in the same remote.

Cons:

- Construction history may still be visible depending on branch strategy.
- Requires strict file selection and verification.

## Separate Repository Option

A clean public release repository can be populated from selected files.

Pros:

- Provides the cleanest reviewer/user-facing surface.
- Avoids exposing construction history and scaffolding by default.

Cons:

- Requires an explicit sync/export process.
- Requires careful tracking back to construction commits for traceability.

## Recommended Default

Prepare an export manifest first. Then choose branch versus separate repository based on maintainer release requirements. If history cleanliness is a hard requirement, prefer a clean public release repository or orphan-style export branch created in a separate approved task.

## Required Pre-export Tasks

- Finalize public README/docs/benchmark spec.
- Add license, citation, contribution, and ignore files.
- Decide which final `repository_spec/` documents are public.
- Curate reports/results retained evidence, if included in v0.
- Implement or explicitly defer user/reproduction scripts.
- Implement or explicitly defer source package and tests.
- Produce a public-surface classification table using `PUBLIC_FINAL`, `PUBLIC_SUPPORT`, `MAINTAINER_ARCHIVE`, `DROP_BEFORE_V0`, and `PRIVATE_ONLY`.

## Export Validation Gates

- Static case-package validator passes on exported cases.
- Public hygiene scan finds no local paths, secrets, prompt/API traces, raw private logs, or private archives.
- `case_sets/` and inventory row counts match approved release scope.
- Denominator values match approved release scaffolds.
- Reports/results, if included, are curated and do not change paper results.
- Future prompts and construction-only audits are absent unless explicitly promoted.
- Top-level release metadata files exist.

## Post-export Checks

- Fresh clone of clean export succeeds.
- Docs links resolve.
- Validator commands run from the clean export.
- No construction-only files are accidentally included.
- Git status is clean after validation.

## Release Tag Prerequisites

- Maintainer approval of clean export contents.
- Validation and hygiene gates passed.
- Denominator and paper-result unchanged statements recorded.
- Release notes identify any deferred components.
- Tag created only after the clean surface is verified.
