# Release-Surface Metadata Readiness v0

## Verdict

Verdict: `ready_with_policy_decisions`.

The repository is ready for a staged release-surface metadata phase, but not for direct release export/tagging. Core benchmark surfaces are in place: Common-core v0 case packages, case-set metadata, external schemas, public Chinese README, user-entry smoke path, user-entry local diagnostics, repository specs, tests, and CI smoke wiring.

Several public release metadata surfaces remain missing or policy-dependent. They should be completed before any release tag or export branch.

## Already Ready

- `README.md` exists and describes SQL-RewriteBench, Common-core v0, smoke commands, user adapters, local output boundaries, optional PostgreSQL diagnostics, and benchmark interpretation boundaries.
- `case_sets/common_core_v0/` exists with 40 Common-core cases and 120 Track A same-engine planned rows.
- Common-core case packages have public READMEs and normalized package structure.
- `schemas/` contains external schema packages for current Common-core cases.
- `docs/` contains user-entry and run-artifact policy documentation.
- `repository_spec/` contains metrics, package, external schema, validation, and public release surface policy material.
- User-entry U0-U7 is closed out as local diagnostic functionality with deferred timing/metrics/paper work.
- CI smoke workflows exist for ledger fixtures and user-entry smoke.

## Main Gaps

- `LICENSE` is missing and requires a maintainer/team license decision.
- `CITATION.cff` is missing and requires authorship, title, version, DOI/URL, and citation policy decisions.
- `CONTRIBUTING.md` is missing and requires contribution policy decisions.
- `benchmark_spec/` is missing; a low-risk skeleton can be created after scope wording is accepted.
- `reports/` and `results/` are missing; public boundary placeholders are safe only if they clearly state that no reports/results migration or paper rendering is performed.
- Root `.gitignore` is missing, although `runs/.gitignore` and CI output cleanup provide partial local-output hygiene.
- Release branch/tag policy remains undecided.

## Recommended Next Safe Action

Collect maintainer decisions for license, citation, contribution policy, README language posture, benchmark-spec wording, reports/results public boundary, and release branch/tag policy. After those decisions are recorded, authorize a metadata-only skeleton task for `benchmark_spec/`, `docs/README.md`, `reports/README.md`, `results/README.md`, and root output-hygiene files as appropriate.
