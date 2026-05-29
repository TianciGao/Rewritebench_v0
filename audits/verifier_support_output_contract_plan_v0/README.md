# verifier_support_output_contract_plan_v0

Verdict: completed.

This packet defines the output contract and integration boundary for future VeriEQL and SQLSolver verifier support in the user-facing local workbench.

Scope:

- Planning/design only.
- VeriEQL included as a future verifier/support tool, not implemented.
- SQLSolver included as a future verifier/support tool, not implemented.
- No verifier tools were run.
- Semantic Equivalence Rate was not computed.

Core boundary:

- VeriEQL and SQLSolver do not generate rewritten SQL.
- They are not rewrite baselines.
- They must not enter same-engine rewrite speedup tables.
- They must not be ranked against methods or routes.
- Their outputs can support Semantic Equivalence Rate only when formal verifier evidence exists.
- Without verifier evidence, Semantic Equivalence Rate remains `N.A.`.

Future output placement:

```text
output/results/<run_id>/verifier/
  verifier_pairs.csv
  verifier_verdicts.jsonl
  semantic_equivalence_summary.json
  tools/
    verieql/
    sqlsolver/

output/logs/<run_id>/verifier.log
output/reports/<run_id>/verifier_summary.md
```

No top-level `reports/` or `results/` surfaces are updated by this plan. Promotion to official evidence remains separately authorized.
