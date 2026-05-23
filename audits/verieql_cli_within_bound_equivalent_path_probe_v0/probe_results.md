# Probe Results

## Final Uppercase Schema Matrix

Timeout per bound run: 30 seconds.

| Bound | Equivalent Pair States | Equivalent Clean EQU | Non-Equivalent Pair States | Clean NEQ |
| ---: | --- | --- | --- | --- |
| 1 | `EQU` | yes | `NEQ` | yes |
| 2 | `EQU,EQU` | yes | `NEQ` | yes |
| 3 | `EQU,EQU,EQU` | yes | `NEQ` | yes |
| 5 | `EQU,EQU,EQU,EQU,EQU` | yes | `NEQ` | yes |
| 10 | `EQU,EQU,EQU,EQU,EQU,EQU,EQU,EQU,EQU,EQU` | yes | `NEQ` | yes |

The equivalent pair was:

```sql
SELECT a FROM T
```

versus:

```sql
SELECT a FROM T
```

The non-equivalent pair was:

```sql
SELECT a FROM T
```

versus:

```sql
SELECT b FROM T
```

## Initial Lowercase Schema Matrix

The initial lowercase schema matrix exposed schema-casing sensitivity:

| Bound | Equivalent Pair States | Non-Equivalent Pair States | Non-Equivalent Error |
| ---: | --- | --- | --- |
| 1 | `EQU` | `OTE` | `'A'` |
| 2 | `EQU,EQU` | `OTE` | `'A'` |
| 3 | `EQU,EQU,EQU` | `OTE` | `'A'` |
| 5 | `EQU,EQU,EQU,EQU,EQU` | `OTE` | `'A'` |
| 10 | `EQU,EQU,EQU,EQU,EQU,EQU,EQU,EQU,EQU,EQU` | `OTE` | `'A'` |

This was not treated as the final verdict because bundled VeriEQL examples use uppercase schema identifiers and the final uppercase schema JSONL resolved the issue.

## Answers

1. `parallel.cli_within_bound` runs successfully with the external VeriEQL venv.
2. `SELECT a FROM T` vs `SELECT a FROM T` produces clean bounded `EQU` with uppercase schema metadata.
3. `SELECT a FROM T` vs `SELECT b FROM T` produces clean `NEQ` with uppercase schema metadata.
4. Clean bounded `EQU` should normalize to local bounded `equivalent` only when all states are `EQU` and no error/timeout/unsupported state appears.
5. This justifies a future finite-bound wrapper mode, but exact-candidate verifier passes should wait until schema canonicalization is implemented and tested.
6. VeriEQL Semantic Equivalence Rate should remain `N.A.` until a separately authorized exact-candidate local verifier pass produces real formal verifier evidence.
