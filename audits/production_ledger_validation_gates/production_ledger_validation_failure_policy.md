# Production Ledger Validation Failure Policy

Status: policy draft, not implementation

## Fail Closed

Production ledger validation must fail closed. If a row cannot be validated safely, the validator should block downstream metrics computation and paper rendering until the issue is corrected or explicitly reviewed.

## No Auto-fix

Validators must not auto-fix production ledger rows. They must not rewrite IDs, infer denominators, fill missing paths, coerce status values, normalize engines by guessing, or edit retained artifact references.

## No Silent Row Dropping

Rows with ambiguous scope, unknown status, missing timing, unsupported engines, or manual-review flags must remain visible in validation reports. Dropping them would hide denominator and evidence coverage issues.

## No Unsafe Coercion

The validator must not:

- coerce `unknown` to `false`;
- coerce `N.A.` to failure;
- fill missing timing with `0`;
- convert `timing_missing` into a zero speedup;
- treat `target_timing_missing` as Speedup Retention failure;
- treat `verifier_unknown` as semantic-equivalence failure without approved policy.

## Manual Review

Rows should require manual review when:

- denominator linkage is ambiguous;
- row grain cannot be determined;
- public hygiene risk is present;
- artifact provenance is unclear;
- retained summary artifacts are being used as if they were metric rows;
- portability or verifier support boundaries are unclear.

## Block Downstream Consumers

Metrics computation, paper table rendering, reproduction CLI outputs, and public runner summaries must be blocked until production ledger validation passes for the relevant scope.

## N.A. Handling

`N.A.` is a valid non-computable state when justified by policy. It is not a failure and is not zero. Future reports should render `N.A.` separately from failures, mismatches, unsupported states, and manual-review states.

## Mutation Boundary

Validation failure reports may be written to an explicit audit directory. The validator must not update the ledger, retained evidence, reports/results, case sets, denominator scaffolds, inventory files, case packages, or raw legacy evidence.
