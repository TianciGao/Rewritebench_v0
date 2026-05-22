# User-Entry Checker Policy

This document describes the current local diagnostic result-checker policy for user-entry runs. It does not define official metrics, paper results, timing/speedup, reports/results updates, retained evidence, or leaderboard output.

## Strict Label Policy

`local_result_checker.py` is strict by default. In same-engine local diagnostic comparisons, result rows are read from JSONL artifacts as JSON objects, and result column labels are the JSON object keys. Those labels are part of exactness today.

Under the current policy, a row where values match but result labels differ remains:

- `checker_status=checker_mismatch`
- `exact_status=mismatch`
- `failure_bucket=mismatch`

This strict behavior applies to explicit aliases by default. A candidate that changes an explicit result alias remains a strict mismatch unless a future case-local or role-local policy explicitly authorizes different behavior.

Generated-expression labels are also not automatically ignored. Engines and adapters may format generated expression labels differently, but the checker does not infer from label text alone that a label is safe to ignore.

## Label-Only Diagnostics

The checker exposes diagnostic fields so local diagnostic output can distinguish value-level mismatches from label-only mismatches:

- `value_exact`
- `label_exact`
- `label_only_mismatch`
- `label_policy`
- `label_mismatch_class`
- `value_mismatch_reason`

`label_only_mismatch=true` means:

- row count matches;
- column count matches;
- multiplicity and row order match under existing normalization;
- normalized values match positionally;
- only result column labels differ.

This is diagnostic visibility only. It is not a correctness relaxation, and it does not make the row exact.

## PORT Diagnostic Boundary

PORT real-adapter rows must remain separate from controlled PORT target-reference diagnostics. A real adapter row reflects the candidate SQL emitted by the adapter under the selected engine. A controlled target-reference diagnostic uses manifest-declared target-reference SQL to validate local role routing and backend/checker plumbing. These role classes should not be merged into a single interpretation.

## Future Policy Changes

Any future exactness-changing label policy must be separately authorized and explicitly case-, role-, or config-gated. It must not globally ignore result labels, and it must preserve row-count, column-count, multiplicity, ordering, and value checks unless a separate explicit policy says otherwise.

Any such future change must also keep local diagnostics separate from:

- denominator changes;
- paper results;
- reports/results migration;
- retained-evidence promotion;
- official metrics;
- timing/speedup;
- leaderboard output.
