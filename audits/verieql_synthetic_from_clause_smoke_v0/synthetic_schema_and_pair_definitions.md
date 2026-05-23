# Synthetic Schema And Pair Definitions

Runtime input directory:

```text
/tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0/input
```

Schema context:

```json
{"T":{"a":"integer","b":"integer"}}
```

The wrapper converted the schema context into the VeriEQL JSONL record as:

```json
{"T":{"A":"INTEGER","B":"INTEGER"}}
```

Pairs executed:

| pair_id | source SQL | candidate SQL | intended interpretation |
| --- | --- | --- | --- |
| `synthetic_from_equivalent` | `SELECT a FROM T;` | `SELECT a FROM T;` | Equivalent smoke pair. |
| `synthetic_from_nonequivalent` | `SELECT a FROM T;` | `SELECT b FROM T;` | Non-equivalent smoke pair. |

Both pairs used:

- `tool=verieql`
- `pair_type=support_pair_smoke`
- `pool=synthetic`
- `engine=synthetic`
- `route_id=verieql_synthetic_smoke`
- `method_id=verieql_support_probe`
- `denominator_id=synthetic_verieql_from_clause_smoke_v0`

No Common-core case files, method-generated candidates, or benchmark denominators were used.
