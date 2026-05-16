# Deferred Or Not-computable Metrics

This file records updated paper-scope metrics or related fields that remain deferred, conditional, or diagnostic. It does not authorize implementation.

## Attribution Coverage

`Attribution Coverage` is the updated explainability metric direction, but implementation is deferred.

Open requirements:

- define what counts as attribution evidence;
- define eligible attribution denominator;
- decide whether plan artifacts, checker evidence, verifier evidence, failure-stage evidence, and curated explanation artifacts are all eligible;
- add or approve ledger fields for attribution type and attribution sufficiency if needed.

## Speedup Retention

`Speedup Retention` belongs to generalization, but it requires paired source/target or source-route/target-route timing.

Policy:

- report `N.A.` when paired target-engine timing is unavailable or unsupported;
- do not treat missing paired timing as zero;
- do not count unsupported target timing as a performance failure without an approved denominator policy.

## Semantic Equivalence Rate

`Semantic Equivalence Rate` depends on verifier decidability and available semantic-equivalence evidence.

Policy:

- verifier evidence is part of correctness discussion;
- verifier support is not an independent Support Layer;
- undecidable or unsupported verifier cases must be reported transparently;
- result consistency remains separate from formal or verifier-supported semantic equivalence.

## Diagnostic Fields

Parseability, extractability, runnable SQL, readiness, unsupported, preflight-blocked, and source-like/no-op status remain diagnostic fields unless separately finalized.

They should support debugging and denominator transparency, but they are not primary metrics in the updated contract.

## Failure Buckets

Failure buckets remain diagnostic only.

Candidate Failure Rate is removed as a primary metric. Failure buckets should not alter Common-core membership, denominator values, or paper results.
