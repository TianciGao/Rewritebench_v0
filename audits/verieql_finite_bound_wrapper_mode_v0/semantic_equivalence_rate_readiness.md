# Semantic Equivalence Rate Readiness

## Current Status

Finite-bound wrapper mode is implemented and synthetic regression-tested.

This makes the code path ready for a separately authorized tiny exact-candidate local verifier pass, provided that pass remains:

- local-only;
- route-aware and denominator-aware;
- exact/result-consistent gated;
- non-official;
- not promoted to top-level reports/results or retained evidence.

## Not Official Yet

Semantic Equivalence Rate is still not official. This task only proves the wrapper can generate clean bounded verifier evidence for synthetic pairs.

Official or paper-facing Semantic Equivalence Rate remains gated on a separate evidence-promotion task.

## Next Implementation Gate

Before broader exact-candidate verification:

- start with one or two exact local candidate rows;
- retain raw verifier JSONL and logs under local output only;
- verify schema context extraction for real cases;
- report unsupported/timeout/tool-error rows separately;
- do not use local result-checker exactness as verifier evidence.
