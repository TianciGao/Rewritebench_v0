# Track A 120 Run Plan

This is the intended future command shape only. It was not executed in this policy task.

## Evaluate command

Run id proposal:

```text
direct_llm_repair_1_track_a_120_canonical_v0
```

Output root proposal:

```text
/tmp/sqlrb_direct_llm_repair_1_track_a_120_canonical_v0/output
```

The future adapter command should be a route-assembly wrapper that:

- reads Direct LLM original canonical row artifacts;
- copies original exact candidates as final Repair-1 candidates without a live call;
- injects original-candidate context and feedback for eligible `mismatch` and `candidate_execution_failed` rows;
- delegates eligible repair rows to `baselines/direct_llm_repair_1/adapter.py`;
- preserves unsupported rows as fail-closed boundary rows; and
- records final route metadata for all 120 rows.

Draft command:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python /tmp/sqlrb_direct_llm_repair_1_track_a_120_canonical_v0/repair1_route_assembly_adapter.py" \
  --output-root /tmp/sqlrb_direct_llm_repair_1_track_a_120_canonical_v0/output \
  --run-id direct_llm_repair_1_track_a_120_canonical_v0 \
  --enable-db-execution \
  --enable-checker \
  --collect-timing
```

Live requirements for the future run:

- `SQLRB_LLM_ALLOW_LIVE=1`
- provider/base URL/model/API-key env present by presence-only review
- no API key value printed or written
- stop on systemic provider access failure such as HTTP 403/code 1010

## Local metrics command

After the future evaluate command completes and only if the run remains within local diagnostic boundaries:

```bash
python -m cli.main user compute-local-metrics \
  --run-id-prefix direct_llm_repair_1_track_a_120_canonical_v0 \
  --engines postgres,mysql,spark \
  --aggregate-run-id direct_llm_repair_1_track_a_120_canonical_v0 \
  --source-run-root runs/user \
  --output-root /tmp/sqlrb_direct_llm_repair_1_track_a_120_canonical_v0/output
```

This command shape is for local diagnostic metrics only. It must not produce official metrics, paper tables, retained-evidence promotion, or leaderboard output.

## User output expectations

User output export/summarize should preserve:

- local-only boundary flags;
- final route candidate metadata;
- verifier status placeholder as `N.A.` when no formal verifier artifacts exist; or
- `coverage_limited` if existing bounded verifier-support evidence is explicitly included.

No verifier tool should run as part of user output export.
