# verieql_cli_within_bound_equivalent_path_probe_v0

Audit date: 2026-05-23

Branch: `feature/case-package-v2-external-schema`

## Verdict

VeriEQL finite-bound batch mode (`parallel.cli_within_bound`) ran successfully with the external VeriEQL venv.

With VeriEQL-compatible uppercase schema metadata for logical table `T(a, b)`, the minimal equivalent pair produced clean bounded `EQU` states for bound sizes 1, 2, 3, 5, and 10. The minimal non-equivalent pair produced clean `NEQ` at each tested bound.

The earlier timeout-mode `EQU...TMO` behavior was primarily a timeout-runner bound-progression issue. Finite-bound mode can produce clean bounded-equivalent local verifier-support evidence for toy pairs.

## Important Caveat

The initial JSONL with lowercase schema column keys produced `OTE` with error `'A'` for the non-equivalent pair. VeriEQL examples and parser behavior expect uppercase schema column keys. A future wrapper extension should canonicalize schema table/column metadata to VeriEQL-compatible casing before exact-candidate verifier passes.

## Boundary

This is local-only VeriEQL tool behavior. It is not Common-core evidence, not method-generated candidate evaluation, not official Semantic Equivalence Rate, not paper evidence, and not retained evidence.
