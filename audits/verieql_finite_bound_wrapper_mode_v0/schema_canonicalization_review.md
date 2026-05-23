# Schema Canonicalization Review

## Reason

The prior finite-bound probe showed that lowercase schema column keys could produce `OTE` with error `'A'` for `SELECT a FROM T` vs `SELECT b FROM T`. With uppercase schema identifiers, VeriEQL returned clean `NEQ`.

## Implemented Behavior

The wrapper now canonicalizes schema identifiers before writing VeriEQL JSONL:

- table identifiers are stripped of quoting and schema prefixes, then uppercased;
- column identifiers are stripped of quoting, then uppercased;
- type strings are uppercased;
- original SQL text and pair metadata remain unchanged and traceable.

Example logical schema:

```json
{"T": {"a": "int", "b": "int"}}
```

VeriEQL JSONL schema:

```json
{"T": {"A": "INT", "B": "INT"}}
```

## Boundary

Repository case SQL files are not rewritten. Canonicalization is limited to verifier JSONL schema metadata.
