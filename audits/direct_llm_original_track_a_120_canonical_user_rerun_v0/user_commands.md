# User Commands

Evaluate:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/direct_llm_original/adapter.py" \
  --output-root /tmp/sqlrb_direct_llm_original_track_a_120_canonical_user_rerun_v0/output \
  --run-id direct_llm_original_track_a_120_canonical_v0 \
  --enable-db-execution \
  --enable-checker \
  --collect-timing
```

Canonical local metrics:

```bash
python -m cli.main user compute-local-metrics \
  --run-id-prefix direct_llm_original_track_a_120_canonical_v0 \
  --engines postgres,mysql,spark \
  --aggregate-run-id direct_llm_original_track_a_120_canonical_v0 \
  --source-run-root runs/user \
  --output-root /tmp/sqlrb_direct_llm_original_track_a_120_canonical_user_rerun_v0/output
```

Run ids:

- `direct_llm_original_track_a_120_canonical_v0__postgres`
- `direct_llm_original_track_a_120_canonical_v0__mysql`
- `direct_llm_original_track_a_120_canonical_v0__spark`
- Aggregate metrics run: `direct_llm_original_track_a_120_canonical_v0`
