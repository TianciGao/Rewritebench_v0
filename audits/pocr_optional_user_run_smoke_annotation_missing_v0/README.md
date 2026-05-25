# POCR Optional User-Run Smoke: Annotation-Missing Mode

This packet records `pocr_optional_user_run_smoke_annotation_missing_v0`.

The smoke exercised the actual user-facing POCR diagnostic CLI path with `--enable-pocr-diagnostic` and no `--annotation-jsonl`, using the existing Direct LLM original PostgreSQL candidate root:

```text
runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql
```

Result:
- User-run smoke executed: yes.
- Rows emitted: 40.
- Annotation-missing rows: 40.
- Temp output root: `/tmp/sqlrb_pocr_user_smoke_annotation_missing_v0/output`.
- Report boundary wording present: yes.

Boundary:
- No live API call.
- No API key read.
- No DB/checker/timing run.
- No baseline rerun.
- No official Positive Operation Coverage Rate computation.
- No route-level POCR aggregation.
- No paper-facing metric promotion.
- No global leaderboard.
- No repository `output/` committed.

Next safe action: add annotation JSONL replay support for the Direct LLM PG40 diagnostic artifact, still default-off and diagnostic-only.
