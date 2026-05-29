# Cross-Verifier Comparison

This comparison is diagnostic only. It does not declare either verifier universally correct.

Existing VeriEQL closeout summary:

- Exact SQLGlot-noop PostgreSQL rows checked: 35.
- Corrected VeriEQL decidable rows after identity guard: 4/35.
- Corrected VeriEQL equivalent/non-equivalent: 4/0.

SQLSolver summary from this pass:

- Exact SQLGlot-noop PostgreSQL rows checked: 35.
- Corrected SQLSolver decidable rows after identity guard: 24/35.
- Corrected SQLSolver equivalent/non-equivalent: 24/0.

`LONGTAIL_0023`:

- VeriEQL: source-vs-source and candidate-vs-candidate identity failed, so the earlier source-vs-candidate non-equivalent result was classified as a VeriEQL identity/modeling diagnostic rather than SQLGlot-noop semantic drift.
- SQLSolver: source-vs-source, candidate-vs-candidate, and source-vs-candidate all returned `EQ`; the row identity-passed and corrected to `equivalent`.

SQLSolver has substantially better local diagnostic coverage on this PostgreSQL noop exact subset than VeriEQL, but the result remains support-layer evidence only.
