# User Command

Case list:

```bash
printf 'CONS_0036\nPERF_0006\n' > /tmp/sqlrb_direct_llm_original_post_user_agent_case_list.txt
```

Command:

```bash
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --case-list /tmp/sqlrb_direct_llm_original_post_user_agent_case_list.txt \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/direct_llm_original/adapter.py" \
  --output-root /tmp/sqlrb_direct_llm_original_bounded_live_api_smoke_post_user_agent_fix_v0/output \
  --run-id direct_llm_original_bounded_live_api_smoke_post_user_agent_fix_v0 \
  --enable-db-execution \
  --enable-checker
```

Run ids:

- `direct_llm_original_bounded_live_api_smoke_post_user_agent_fix_v0__postgres`
- `direct_llm_original_bounded_live_api_smoke_post_user_agent_fix_v0__mysql`
- `direct_llm_original_bounded_live_api_smoke_post_user_agent_fix_v0__spark`

Command result:

```text
postgres: selected_rows=2, candidate_generated_rows=2
mysql: selected_rows=2, candidate_generated_rows=2
spark: selected_rows=2, candidate_generated_rows=2
exit_code=0
```

