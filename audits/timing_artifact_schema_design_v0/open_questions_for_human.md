# Open Questions For Human Confirmation

1. Should local timing diagnostics be allowed for non-official user adapter runs before retained-evidence promotion?
2. Should timing sample arrays be JSON arrays in JSONL, or separate per-row files referenced by path?
3. Should timing artifacts store source/candidate SQL hashes?
4. Should source timing be remeasured for every candidate route, or can source timing be reused within one local run if schema/session/cache policy is identical?
5. What cache policy should be default for local diagnostics?
6. How should partial timing sample failure be handled?
7. Should label-only mismatch rows always be timing-ineligible under the strict current policy?
8. How should target-engine timing be represented for Cross-Engine GM Speedup Ratio?
9. What is the promotion gate from local timing artifacts to official retained timing evidence?
10. How should future summaries prevent route mixing?

## Additional Alignment Questions Carried Forward

- Does Execution Coverage Rate require source execution success in the same row, or only candidate execution success among planned rows?
- Should Result Consistency Rate use planned denominator `N_S` exactly as the latest formula indicates?
- Is Semantic Equivalence Rate N.A. unless verifier evidence exists?
- Does Cross-Engine GM Speedup Ratio fully replace Speedup Retention?
- Should Regression@20 remain a reporting diagnostic rather than a latest-paper Table 6 metric?
