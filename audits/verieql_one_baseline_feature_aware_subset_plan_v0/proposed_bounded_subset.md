# Proposed Bounded Subset

Subset CSV:
- `proposed_bounded_subset.csv`

Recommended next actual pass:

| order | case_id | role | precondition | attempt |
| ---: | --- | --- | --- | --- |
| 1 | CONS_0036 | positive control | can run now | yes |
| 2 | CONS_0037 | first expansion candidate | after DDL parser hardening | yes after hardening |

Rationale:
- `CONS_0036` is the only currently proven real exact source-vs-candidate row with clean all-`EQU`.
- `CONS_0037` is the closest next row by static feature scan: single SELECT, no `LIKE`, no `EXISTS`, no nested subquery, no date/time literal, no window function, and no dialect quoting/LIMIT risk.
- `CONS_0037` should wait for DDL parser hardening because its schema contains `VARCHAR(32)`.

Rows not recommended for the next pass:
- `PERF_0077` and `PERF_0082`: already known `LIKE` -> `NIE`.
- `CONS_0007`: already known `EXISTS` unsupported.
- PORT quoted/LIMIT rows: need a dialect-syntax probe first.
- TPC-H/TPC-DS date/time/function-heavy rows: need feature-specific probes first.

Readiness:
- Ready for a bounded one-baseline verifier pass only after DDL parser hardening.
- Without that hardening, the only safe real candidate is repeating `CONS_0036`, which is not enough to broaden coverage.

