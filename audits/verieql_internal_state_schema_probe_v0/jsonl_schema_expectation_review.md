# JSONL Schema Expectation Review

## Batch CLI

The staged VeriEQL README documents batch timeout invocation in this shape:

```bash
python -m parallel.cli_within_timeout -f <pairs.jsonl> -t <timeout> -o <output.jsonl>
```

The code path in `parallel/cli_within_timeout.py` reads each JSONL object and consumes these fields:

- `index`
- `schema`
- `constraint`
- `pair`
- `contain_unsupported_constraints`, when present
- metadata such as `file`, `name`, and `benchmark`

Extra fields are tolerated because the runner keeps the whole record as a context object and reads only the fields it needs.

## Shipped Benchmark Shape

Shipped benchmark JSONL files under `benchmarks/` use records with fields such as:

- `index`
- `schema`
- `constraint`
- `pair`
- `file`
- `name`
- `benchmark`
- `contain_unsupported_constraints`, in some records

The release wrapper's generated records include the same required execution fields plus SQL-RewriteBench traceability fields:

- `pair_id`
- `case_id`
- `pair_type`
- `pair_role`

Those extra traceability fields do not appear to break VeriEQL parsing.

## Schema Field

The batch runner expects `schema` to be a mapping from table name to columns. The local synthetic smoke used a minimal schema equivalent to:

```json
{
  "T": {
    "a": "int",
    "b": "int"
  }
}
```

The direct API creates symbolic rows from this schema and adds type constraints. The missing clean equivalent result is therefore not explained by a required table schema being absent.

## Constraint Field

`constraint` may be absent, null, or an array. If present and not marked unsupported, the timeout runner calls `env.add_constraints(...)`. Constraints can encode primary keys, foreign keys, inclusion, nullability, ranges, and comparison predicates.

The minimal synthetic smoke did not require obvious semantic constraints for `SELECT a FROM T` vs `SELECT a FROM T`, so missing constraints are not the most likely root cause. They may still affect bound progression and solver performance for larger examples.

## Current Wrapper Fit

The wrapper-generated JSONL matches the batch runner's expected shape closely enough for real invocation:

- CONS_0007 reached VeriEQL and returned `NSE` for `EXISTS`.
- PERF_0062 reached VeriEQL and returned `EQU,TMO`.
- Synthetic `SELECT 1` pairs reached VeriEQL and returned `NSE` for missing `FROM`.
- Synthetic `FROM` pairs reached VeriEQL and returned `EQU,TMO` or `NEQ`.

These outcomes indicate the wrapper is invoking the tool and passing parseable JSONL. No immediate input-format bug was found.
