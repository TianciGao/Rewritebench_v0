# Provider Metadata Review

Provider/model policy was confirmed by environment presence and row metadata without printing secret values.

- provider: `openai_compatible`
- model: `gpt-5.4`
- live gate: enabled
- raw responses saved: false
- adapted route metadata: `adapted_gpt54_local_diagnostic=true`
- original paper reproduction: false
- official R-Bot stack: false
- fake runtime: false
- live call: true for all 40 selected rows
- retrieval used: false for all 40 selected rows
- RAG index used: false for all 40 selected rows
- CalciteRewrite used: false for all 40 selected rows
- no secret values: true

All 40 `rbot_status.json` metadata records had provider `openai_compatible`, model `gpt-5.4`, `runtime_status=live_provider_success`, `extraction_status=extracted`, `live_call=true`, `fake_runtime=false`, `retrieval_used=false`, `rag_index_used=false`, `calcite_rewrite_used=false`, and `raw_response_saved=false`.
