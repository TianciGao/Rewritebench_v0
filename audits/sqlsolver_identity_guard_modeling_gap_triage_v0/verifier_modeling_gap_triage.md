# Verifier Modeling Gap Triage

## Why Identity Unknown Blocks SER Promotion

Identity guards check whether SQLSolver can prove a query equivalent to itself before interpreting source-vs-candidate evidence. Five of eight selected pairs returned `unknown` on at least one identity guard. A source-candidate verdict for those rows would be uninterpretable: the verifier has not shown it can model even the identity form of the row. These rows must remain outside any decidable SER denominator and be reported separately.

## Method vs Verifier Boundary

The five unknown identity guards are verifier/modeling limitations, not SQLGlot no-op rewrite-method failures. All eight selected pairs came from exact/result-consistent local checker rows, and the unknowns occurred on source-vs-source or candidate-vs-candidate guards before source-vs-candidate interpretation.

## Should SQLSolver Be Expanded Now?

No. The bounded pass found useful positive evidence for three rows, but the identity-guard unknown rate is too high for a larger pass to produce clean verifier-support evidence. Expanding now would mostly produce mixed unknown coverage without resolving whether failures come from SQLSolver feature support, wrapper normalization, schema canonicalization, or dialect syntax.

## Needed Fixes Before Expansion

- Define wrapper canonicalization for leading `--` comments and line-comment collapse.
- Decide whether to normalize PostgreSQL DATE and INTERVAL syntax before SQLSolver.
- Canonicalize schema DDL comments and PostgreSQL-specific types such as `DOUBLE PRECISION` when passing to SQLSolver.
- Decide whether quoted identifiers and `NULLS FIRST/LAST` PORT rows are in or out of the first SQLSolver support scope.
- Add feature-support canaries for DENSE_RANK/CTE ranking separately from benchmark evidence.

## VeriEQL Position

VeriEQL should wait. This SQLSolver-first pass already exposed identity-guard modeling gaps. Adding VeriEQL now would broaden the surface before resolving the basic verifier-pair modeling policy.

## Recommended Next Safe Action

Write a narrow wrapper/schema canonicalization design packet for SQLSolver identity guards. The first implementation task should be a non-benchmark fixture/canary layer, not a larger Track A pass and not SER promotion.
