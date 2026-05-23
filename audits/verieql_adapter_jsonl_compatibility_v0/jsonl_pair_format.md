# JSONL Pair Format

## Generated Input Shape

Each generated line is a JSON object shaped for the discovered VeriEQL batch expectation:

```json
{
  "index": 1,
  "file": "CONS_0007:source_positive:cons0007_source_positive",
  "name": "CONS_0007:source_positive:cons0007_source_positive",
  "benchmark": "CONS_0007:source_positive",
  "case_id": "CONS_0007",
  "pair_id": "cons0007_source_positive",
  "pair_type": "source_vs_positive",
  "pair_role": "source_positive",
  "schema": {},
  "constraint": [],
  "pair": ["<source sql>", "<comparison sql>"]
}
```

## Pair Role Mapping

| verifier pair_type | VeriEQL pair_role |
|---|---|
| `source_vs_candidate` | `source_candidate` |
| `source_vs_candidate_port_target` | `source_candidate_port_target` |
| `source_vs_positive` | `source_positive` |
| `source_vs_hard_negative` | `source_negative` |
| `support_pair_smoke` | `support_pair_smoke` |

## Schema Handling

If `schema_context_path` points to JSON, the wrapper uses that object as table/column/type metadata.

If it points to SQL DDL, the wrapper performs a narrow best-effort `CREATE TABLE` parser to produce:

```json
{
  "TABLE": {
    "COLUMN": "TYPE"
  }
}
```

If no schema is available or parsing fails, schema is `{}` and the verifier remains responsible for accepting or rejecting the input. No constraints are inferred.

## Constraint Policy

`constraint` is always `[]` in this compatibility layer. No PK/FK/UNIQUE constraints are inferred from SQL, taxonomy, case metadata, or checker configuration.
