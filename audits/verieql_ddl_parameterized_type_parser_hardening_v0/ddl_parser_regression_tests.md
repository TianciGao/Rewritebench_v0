# DDL Parser Regression Tests

Focused tests added in `tests/user_entry/test_verieql_support.py`:
- `CREATE TABLE T (A VARCHAR(32));`
- `CREATE TABLE T (A NUMERIC(15,2));`
- `CREATE TABLE T (A DECIMAL(9,2));`
- `CREATE TABLE public.t (a INTEGER, b VARCHAR(32), c NUMERIC(15,2));`
- Existing JSONL generation test now asserts `VARCHAR(10)` is preserved.

Focused test result:

```text
pytest tests/user_entry/test_verieql_support.py -q
20 passed, 3 subtests passed
```

The tests confirm:
- full parameterized type strings are preserved;
- simple integer type parsing still works;
- identifiers remain canonicalized to uppercase metadata;
- JSONL schema output includes the preserved type string.

Repository-local parser scan:
- Exact rows scanned from `runs/user/common_core_pg_noop_db_checker`: 35.
- Rows with parameterized DDL types: 17.
- Rows with malformed/truncated type metadata after hardening: 0.
