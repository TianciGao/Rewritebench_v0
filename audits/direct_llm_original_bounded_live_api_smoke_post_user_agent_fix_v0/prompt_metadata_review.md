# Prompt Metadata Review

Secret-free adapter metadata observed across all 6 row status files:

```text
provider=openai_compatible
base_url_host=api.gptsapi.net
model_id=gpt-5.4
temperature=0.0
top_p=1.0
max_tokens=2048
timeout_seconds=60.0
prompt_template_id=direct_llm_original_sql_only_v0
extraction_policy=single_sql_candidate_v0
live_call=true
user_agent_present=true
raw_response_saved=false
local_only=true
official_metric_input=false
paper_result=false
```

The adapter source at this commit sends `User-Agent: SQL-RewriteBench/0.1` for OpenAI-compatible calls. Raw provider responses were not saved.

