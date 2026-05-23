# user_verify_facade_fail_closed_v0

Verdict: completed.

Implemented a local-only `sqlrb user verify` CLI facade for bounded verifier support.

Commands added:

```bash
sqlrb user verify --run-id <run_id> --tool verieql --output-root output
sqlrb user verify --run-id <run_id> --tool sqlsolver --output-root output
```

The command writes D035-shaped verifier artifacts under:

- `output/results/<run_id>/verifier/`
- `output/logs/<run_id>/verifier.log`
- `output/reports/<run_id>/verifier_summary.md`

The facade uses synthetic smoke pairs only in this phase. When the selected verifier tool is unavailable, the command fails closed with `not_attempted` verdict rows and `semantic_equivalence_rate=null`.

No real VeriEQL or SQLSolver command was required or installed. No official Semantic Equivalence Rate, official metrics, top-level reports/results, retained evidence, or leaderboard output was produced.
