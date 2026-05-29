# Direct LLM Repair-1 Track A 120 Canonical User Rerun

This packet records the Direct LLM + Repair-1 Track A 120 canonical local diagnostic run using the approved route assembly policy.

Run id: `direct_llm_repair_1_track_a_120_canonical_v0`

Source route assembly:

- original exact rows replayed as final original candidates: 102
- repair attempted rows: 13
- unsupported rows preserved: 5
- final candidate source counts: {'original': 102, 'repaired': 13, 'unsupported_or_none': 5}

Canonical local metrics were computed only through:

```bash
python -m cli.main user compute-local-metrics
```

Overall local diagnostic metrics:

- selected: 120
- generated: 120
- candidate executable: 115
- exact: 111
- timed: 98
- generation rate: 1.0
- execution coverage: 0.9583333333333334
- result consistency: 0.925
- GM speedup: 0.9978498743494606

Boundary: no SQLSolver, VeriEQL, official metrics, paper rendering, retained evidence promotion, or leaderboard generation occurred.

Next safe action: review this Repair-1 Track A 120 local diagnostic against Direct LLM original with role-aware, denominator-aware local evidence only.
