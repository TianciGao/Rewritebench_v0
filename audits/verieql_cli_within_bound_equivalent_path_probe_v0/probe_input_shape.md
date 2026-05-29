# Probe Input Shape

## Runtime Directory

All runtime files were written under:

`/tmp/sqlrb_verieql_cli_within_bound_equivalent_path_probe_v0/`

No repository-level `output/` or `runs/user/` artifacts were created or committed.

## Logical Schema

Both input files represent the same logical schema:

- table `T`
- integer column `a`
- integer column `b`

## Initial Lowercase Schema JSONL

The initial input used lowercase column keys:

```json
{
  "schema": {
    "T": {
      "a": "INT",
      "b": "INT"
    }
  },
  "constraint": [],
  "pair": ["SELECT a FROM T", "SELECT b FROM T"]
}
```

This produced clean `EQU` for the identical pair, but the non-equivalent pair returned `OTE` with error `'A'`. That indicates a column-key casing mismatch against VeriEQL's internal uppercase identifier handling.

## Final Uppercase Schema JSONL

The final input used uppercase schema keys, matching VeriEQL bundled examples:

```json
{
  "schema": {
    "T": {
      "A": "INT",
      "B": "INT"
    }
  },
  "constraint": [],
  "pair": ["SELECT a FROM T", "SELECT b FROM T"]
}
```

This produced the desired clean bounded results:

- identical pair: all `EQU`;
- column-difference pair: `NEQ`.

## Wrapper Implication

The command and JSONL record shape are valid. Before using VeriEQL on exact candidates, the wrapper should canonicalize schema identifiers to VeriEQL-compatible casing and retain the original SQL and schema paths for traceability.
