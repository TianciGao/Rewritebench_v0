# VeriEQL Feature-Support Notes

Sources inspected:

- `/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL/README.md`
- VeriEQL Python sources under the staged root
- Prior `CONS_0007` canary raw output

README-level support statement:

- VeriEQL documents batch JSONL use through `python -m parallel.cli_within_timeout -f <jsonlines> -t <timeout> -o <out>`.
- The README describes supported semantics as list semantics for `ORDER BY` and bag semantics.
- The README does not provide a complete textual unsupported-feature matrix.

Confirmed unsupported by local canary:

- `EXISTS`: `CONS_0007` returned `states=["NSE"]` and `err="Not supported feature: EXISTS"`.

Source-level unsupported or high-risk features:

- `EXISTS` is explicitly raised as `NotSupportedError('EXISTS')` in the encoder.
- Window `OVER` is explicitly raised as unsupported.
- Subquery in a `SELECT` clause is explicitly raised as unsupported.
- Query-in-`SELECT` paths are explicitly raised as unsupported.
- `TIMESTAMPDIFF` is limited; non-DAY units are rejected.
- Interval handling is limited to DAY interval.
- Some date formats are rejected.
- `stddev_pop`, `var_pop`, `stddev_samp`, and `var_samp` are rejected as unsupported.
- `IFNULL` containing a table is rejected.
- Some `COUNT` expression forms are not implemented.
- `IN` / `NOT IN` predicate formula code can reject uninterpreted-function cases.
- Outer join formula code contains unsupported corner cases.
- Parser comments mention several disabled unsupported checks, including `EXISTS`, `GROUPING`, `SUBSTRING`, `LATERAL`, `EXTRACT`, `ROLLUP`, `LIKE`, and `TRIM`; because these are comments, they were treated as weak risk signals, not hard evidence.

Likely safer next-canary shape:

- One `SELECT` per side.
- No `EXISTS` or `NOT EXISTS`.
- No nested `SELECT`.
- No scalar subquery.
- No window `OVER`.
- No date/time/interval expressions.
- No outer joins.
- No set operations.
- Prefer simple projection/filter/join/aggregate over richer SQL features.

Important caveat:

- Static feature screening is only a support-risk triage. It is not verifier evidence and does not establish semantic equivalence.
