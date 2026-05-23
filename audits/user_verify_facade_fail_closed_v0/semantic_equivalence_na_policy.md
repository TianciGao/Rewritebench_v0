# Semantic Equivalence N.A. Policy

This task does not compute official Semantic Equivalence Rate.

Current behavior:

- If the verifier tool is unavailable, the summary rate is `null`.
- If no decidable verifier outcomes exist, the summary rate is `null`.
- Unknown, timeout, unsupported, tool-error, and not-attempted outcomes are reported separately.
- Local result-checker exactness is not verifier evidence.
- Synthetic test and smoke summaries are local diagnostics only.

Future real-tool runs may produce local diagnostic semantic-equivalence summaries over bounded verifier evidence, but official promotion remains separately authorized.
