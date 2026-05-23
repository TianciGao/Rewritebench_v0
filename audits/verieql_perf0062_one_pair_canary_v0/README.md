# VeriEQL PERF_0062 One-Pair Canary V0

Task: `verieql_perf0062_one_pair_canary_v0`

Branch: `feature/case-package-v2-external-schema`

Verdict: `canary_ran_timeout_no_decidable_verdict`

This task ran exactly one bounded local VeriEQL canary:

- Tool: VeriEQL
- Case: `PERF_0062`
- Pair: `source_vs_positive`
- Positive: `pos_01`
- Runtime output root: `/tmp/sqlrb_verieql_perf0062_one_pair_canary_v0`

The staged VeriEQL batch invocation completed and wrote output JSONL. The tool-native row reported:

```text
states=["EQU","TMO"]
err=null
```

The shared wrapper normalized the verdict to:

```text
timeout
```

Reason: a `TMO` state was present, so the row is not treated as a decidable equivalence verdict.

The local `semantic_equivalence_summary.json` remained:

```text
semantic_equivalence_rate=null
semantic_equivalence_rate_status=not_applicable
decidable_count=0
timeout_count=1
result_checker_exactness_used=false
```

This is local verifier-support evidence only. It is not official Semantic Equivalence Rate, not paper evidence, not retained evidence, and not leaderboard input.
