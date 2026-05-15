# Draft Witness Rows

This directory contains draft-only witness rows for `PORT_0004`.

- These rows have not been loaded into any engine.
- They are planning artifacts for later cross-engine validation.
- The row mix is designed to make the 1980 vs 1981 year predicate materially observable in the aggregate percentage.

Before later validation, a human or Codex task should:

1. confirm the row set against the source and rewrite SQL,
2. translate the rows into engine-specific load statements if needed,
3. verify that source and positive match on the 1980 subset,
4. verify that the hard negative diverges on the 1981 boundary row.
