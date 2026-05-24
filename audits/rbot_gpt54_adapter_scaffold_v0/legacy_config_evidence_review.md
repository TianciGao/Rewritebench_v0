# Legacy Config Evidence Review

## Legacy Paths Inspected

Read-only searches were run under:

- `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean/reports/evaluation/common_core_v0/`
- online legacy reference: `https://github.com/TianciGao/sql-rewrite-bench/tree/artifact/case-package-contract-alignment-clean/reports/evaluation/common_core_v0`

Search terms included `R-Bot`, `rbot`, `LLM4Rewrite`, `my_rewriter`, `logs_gpt3`, `logs_llm_only`, `logs_learned_rewrite`, `r_bot`, `RBot`, `PG15`, `mixed-scope`, `formal 120`, and `bounded`.

## Clues Found

Legacy files include:

- `r_bot_120_preflight_v1.md`
- `r_bot_upstream_runner_alignment_audit_v1.md`
- `r_bot_common_core_120_evidence_reconciliation_v1.csv`
- `r_bot_formal_protocol/`
- `r_bot_formal_substrate_freeze_01/`
- historical run roots under `runs/r_bot_*`

The legacy evidence shows a formal 120 planning line, but the recovered runner was not benchmark-ready. PostgreSQL generation/execution/timing evidence is bounded and partial; MySQL/Spark rows were not executable evidence for a tri-engine route.

## Official Source Clues

The official `curtis-sun/LLM4Rewrite` README describes:

- OpenAI API key setup.
- configurable database settings.
- RAG based on LlamaIndex and Chroma.
- `my_rewriter/test.sh` benchmark entrypoints.
- `CalciteRewrite/` for rule-based rewrites using Apache Calcite.
- logs such as `logs`, `logs_gpt3`, `logs_llm_only`, and `logs_learned_rewrite`.

These clues inform future wrapper boundaries only. They were not copied, executed, or vendored.
