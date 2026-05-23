# Output Parser Review

## Parser Inputs

The parser reads VeriEQL JSONL output records by integer `index`.

Expected output fields may include:

- `index`
- `states`
- `err`
- `counterexample`
- `pair`
- `schema`
- `constraint`

## Normalization

The wrapper maps output records as follows:

| VeriEQL signal | normalized verdict |
|---|---|
| final `EQU` / `EQ` state with no error | `equivalent` |
| `NEQ`, counterexample, or not-equivalent text | `non_equivalent` |
| `TMO`, timeout text | `timeout` |
| `NSE`, unsupported, not-supported text | `unsupported` |
| explicit unknown/undecidable text | `unknown` |
| error text with no recognized verdict | `tool_error` |
| missing output row | `tool_error` |

Unknown, timeout, unsupported, tool-error, and not-attempted rows are excluded from the decidable denominator by the shared summary generator.

## Semantic Equivalence Rate Policy

The wrapper computes only local diagnostic summaries from actual normalized verifier rows. It does not use local result-checker exactness as verifier evidence, and it does not compute official Semantic Equivalence Rate.
