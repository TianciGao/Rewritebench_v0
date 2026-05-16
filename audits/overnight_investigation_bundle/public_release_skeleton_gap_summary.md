# Public Release Skeleton Gap Summary

Date: 2026-05-17

## Scope

This audit compares the current public release repository to the intended clean release layout. No missing files or directories were created.

## Must Add Before Release v0

- `README.md`: current_exists=true; create public-facing README after docs direction is approved
- `LICENSE`: current_exists=false; add explicit release license after maintainer confirmation
- `.gitignore`: current_exists=false; add/confirm ignores for local runs and generated outputs
- `benchmark_spec/`: current_exists=false; formalize public benchmark_spec from current specs/decisions
- `scripts/user/`: current_exists=false; create only during runner design/implementation task
- `scripts/reproduce/`: current_exists=false; create only after ledger/metrics contract is ready
- `docs/`: current_exists=false; create docs map, quickstart, case-package guide, retained evidence notes

## Should Add Before Release v0

- `CITATION.cff`: current_exists=false; add citation metadata before public tag
- `CONTRIBUTING.md`: current_exists=false; add lightweight contribution guide
- `pyproject.toml`: current_exists=false; create when src/scripts packaging starts
- `taxonomy/`: current_exists=false; create or defer with explicit note
- `scripts/metrics/`: current_exists=false; create only after metric implementation is authorized
- `reports/`: current_exists=false; do not populate until retained evidence triage is approved
- `results/`: current_exists=false; do not populate until curated results migration is approved
- `tests/`: current_exists=false; add CI smoke after src/scripts interfaces exist
- `src/`: current_exists=false; create when adapter/runner implementation is authorized
- `.github/workflows/`: current_exists=false; add after tests and commands are stable

## Optional Or Deferred Items

- `Makefile`: current_exists=false; add only after stable commands exist
- `baselines/`: current_exists=false; create only if public baseline wrappers are selected

## Recommended Order

1. Create a public README/docs/benchmark_spec skeleton that explains the Common-core 40 boundary and redevelopment roadmap.
2. Add license, citation, contributing, and `.gitignore` hygiene files after maintainer confirmation.
3. Formalize script namespaces only after runner/output policy and metrics contract decisions are implementation-ready.
4. Add `src/`, tests, and CI together with the first retained-evidence adapter or runner skeleton.
5. Populate `reports/` and `results/` only after retained-evidence triage selects public-safe artifacts.

## Relation To Clean Layout Plan

The current repository has canonical case packages, registry scaffolds, project controls, and draft specs. It does not yet have the public user documentation, finalized benchmark spec namespace, package implementation, CI, or curated report/result surfaces expected for a complete clean release.
