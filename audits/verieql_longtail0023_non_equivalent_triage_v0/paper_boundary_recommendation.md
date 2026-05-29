# Paper Boundary Recommendation

Recommendation:

- Do not promote the `LONGTAIL_0023` `non_equivalent` result to paper-facing Semantic Equivalence Rate evidence.
- Keep the all-exact bound-4 PostgreSQL SQLGlot-noop ledger local-only and coverage-limited.
- Treat `LONGTAIL_0023` as blocking paper-facing Semantic Equivalence Rate promotion until the identity-pair VeriEQL failure is explained or the row is excluded under a separately authorized, durable verifier eligibility policy.

Reason:

- Source and candidate SQL are byte-identical.
- VeriEQL reports `non_equivalent` for source-vs-source and candidate-vs-candidate at bound 4.
- This violates the expected identity property for the exact SQL shape.

Next safe action:

- Plan a VeriEQL identity-invariant/tool-semantics audit for CTE + aggregate + outer join + null cases.
- Keep official Semantic Equivalence Rate N.A. or coverage-limited until the verifier eligibility policy addresses this class.
