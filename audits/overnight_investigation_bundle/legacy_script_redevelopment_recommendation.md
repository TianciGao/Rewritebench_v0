# Legacy Script Redevelopment Recommendation

Date: 2026-05-17

## Scope

This recommendation summarizes a read-only inventory of legacy `scripts/`, `tools/`, and `baselines/` paths. No scripts were copied, refactored, or implemented.

## Useful References

- `wrap_candidate`: scripts that may be useful as behavior references behind new public interfaces after output policy review.
- `refactor_candidate`: scripts whose logic may inform future modules but should be rewritten around canonical case packages, case sets, and the evidence ledger.
- `reference_only`: helper or one-off scripts that are useful context but not public architecture.
- `manual_review_required`: scripts with LLM/API/prompt/token terms, local-output risks, or ambiguous public suitability.
- `archive_candidate`: scratch or legacy-specific scripts that should not be copied into the clean public workbench by default.

## Classification Counts

- `refactor_candidate`: 27
- `reference_only`: 68
- `wrap_candidate`: 28

## Recommended Future Layers

- `baselines`: 1
- `scripts/dev`: 91
- `scripts/metrics`: 2
- `scripts/reproduce`: 28
- `src/sql_rewrite_bench`: 1


## What To Wrap

Wrap only stable behaviors that map cleanly to canonical packages and the output policy: environment checks, static validators, package preflights, and selected retained-evidence readers. Wrapper candidates must not write into case-local `runs/` by default.

## What To Refactor

Refactor report, metric, plan collection, checker, and reproduction logic into a new workbench architecture. Future modules should read case sets, inventory, case manifests, and ledger rows rather than hard-coded legacy workspace paths.

## What To Archive Or Drop

Do not copy raw one-off report renderers, local run workspace scripts, LLM/API helpers, or scratch/debug scripts into the public architecture without review. Treat them as private/archive references unless a future design selects a public-safe subset.

## Suggested Implementation Order

1. Formalize benchmark spec and public output policy.
2. Design retained evidence adapter interfaces and validation tests.
3. Build non-mutating ledger reader/builder skeleton after adapter approval.
4. Implement metrics only after the updated metric contract is approved for implementation.
5. Add user/reproduction runners after output-root and user-submission formats are settled.

## Metric/Runner Blocker

Metrics and unified runner work still depend on approved metric semantics, retained-evidence adapter design, and final output-root policy. This audit does not authorize implementation.
