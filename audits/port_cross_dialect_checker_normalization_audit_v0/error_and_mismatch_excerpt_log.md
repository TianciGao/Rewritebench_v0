# Error And Mismatch Excerpt Log

No source-reference execution errors, PostgreSQL target-candidate execution errors, schema setup errors, connection errors, or checker runtime errors were observed in the inspected controlled diagnostic artifacts.

Short mismatch excerpts are redacted to values and column labels only. Local absolute paths, connection details, and setup scripts are omitted.

| Case | Source Excerpt | Target Excerpt | Audit Classification |
|---|---|---|---|
| `PORT_0004` | expression-labeled scalar -> `50` | `?column?` -> `50` | column-label normalization gap |
| `PORT_0013` | expression-labeled scalar -> `66.66666666666667` | `?column?` -> `66.66666666666667` | column-label normalization gap |
| `PORT_0022` | expression-labeled scalar -> `0.25` | `?column?` -> `0.25000000000000000000` | column-label plus decimal-string normalization gap |
| `PORT_0024` | expression-labeled scalar -> `50` | `?column?` -> `50.0000000000000000` | column-label plus decimal-string normalization gap |
| `PORT_0025` | `account_id` -> `2` | `account_id` -> `2` | exact comparison |

The four mismatch rows all have one source row and one target row. After ignoring the single output column label, `PORT_0004` and `PORT_0013` have identical string values, while `PORT_0022` and `PORT_0024` have decimal-equivalent values.
