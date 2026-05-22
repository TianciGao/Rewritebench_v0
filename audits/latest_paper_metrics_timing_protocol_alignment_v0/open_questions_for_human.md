# Open Questions For Human/Team Confirmation

1. Should Regression@20 remain a reporting diagnostic even though it is not in latest Table 6?
2. Is `candidate_generated` raw adapter output, or should preflight/ready be separately reported?
3. Does Execution Coverage Rate require source execution success in the same row, or only candidate execution success among planned rows?
4. Is Semantic Equivalence Rate N.A. unless verifier evidence exists?
5. How will `C_r` for POCR be selected and versioned?
6. What Stage B evidence is required for POCR?
7. Does Cross-Engine GM Speedup Ratio fully replace Speedup Retention?
8. Does target-engine source timing require paired target-engine source/reference execution in the same run?
9. Are local timing diagnostics allowed before official retained-evidence promotion?
10. What gate promotes local timing artifacts to official paper evidence?

## Highest-Priority Blocking Questions

- Confirm whether Result Consistency Rate uses planned denominator `N_S` per latest formula or executed denominator as in the older repository contract.
- Confirm whether `E_r` means candidate execution success or execution attempted.
- Confirm whether POCR operation atom schema will be repository-owned, external-script-owned, or jointly versioned.
