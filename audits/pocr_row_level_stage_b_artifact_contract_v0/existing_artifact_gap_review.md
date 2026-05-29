# Existing Artifact Gap Review

The Repair-1 dry-run row-level source depended on a local `/tmp` replay CSV:

```text
/tmp/sqlrb_pocr_user_replay_direct_llm_repair1_pg40_targeted_retry_v0/output/results/pocr_user_replay_direct_llm_repair1_pg40_targeted_retry_v0/pocr/diagnostic_rows.csv
```

That file contained the decisive per-row expected atom counts and Stage-B-supported counts needed for macro-average. The committed Repair-1 audit packets had useful summaries and mapping rows, but not a complete durable row-level Stage B metrics file with every field needed by the D039 aggregator.

SQLGlot no-op had a committed row-level sanity-control review CSV and local `/tmp` replay row CSV. The local replay CSV was still the most complete row-level source because it preserved replay flags and annotation fail-closed status.

Committed audit packet sufficiency gap:

- Aggregate summaries cannot reconstruct macro-average.
- Mapping rows cannot reconstruct per-row `OC_i`.
- Stage A annotation JSONL is not Stage B row metrics.
- Local `/tmp` replay CSVs are not durable enough for public or reviewer reproduction.

Future replay/exporter work should write durable row-level Stage B metrics under D035:

```text
output/results/<run_id>/pocr/stage_b/pocr_stage_b_row_metrics.csv
```

Public or reviewer reproduction cannot rely on `/tmp` because `/tmp` is local, transient, and not a stable artifact identity layer.

Aggregator must not rely on /tmp replay artifacts.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
