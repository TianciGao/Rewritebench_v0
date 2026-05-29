# Verdict Normalization Recommendation

## Clean Bounded Equivalent

For finite-bound mode, normalize a row to local bounded `equivalent` only if:

- every returned state is `EQU`;
- at least one state is present;
- no `TMO`, `NSE`, `UNK`, `SYN`, `NIE`, `OOM`, or `OTE` appears;
- `err` is null or empty.

The output must retain:

- the requested max bound;
- the full state list;
- per-bound timing values;
- schema/constraint metadata pointers;
- local-only boundary flags.

## Clean Non-Equivalent

Normalize a row to `non_equivalent` if:

- `NEQ` appears in the state list;
- a counterexample or non-equivalence error is recorded when available.

For this local probe, `SELECT a FROM T` vs `SELECT b FROM T` produced clean `NEQ`.

## Ambiguous Or Failed States

Keep these separately visible:

- `TMO`: timeout
- `NSE`: unsupported
- `UNK`: unknown
- `SYN`: syntax error
- `NIE`: not implemented
- `OOM`: out of memory
- `OTE`: other tool error

Do not reinterpret `EQU...TMO` as equivalent.

## Local Boundary

Clean bounded toy `EQU` is tool-behavior evidence only. It does not compute official Semantic Equivalence Rate and does not authorize paper evidence or retained-evidence promotion.
