# Legacy Script Evidence Review

## Paths Inspected

Read-only local legacy path:

- `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean/reports/evaluation/common_core_v0/`

Online legacy reference:

- `https://github.com/TianciGao/sql-rewrite-bench/tree/artifact/case-package-contract-alignment-clean/reports/evaluation/common_core_v0`

Official references:

- `https://github.com/DAMO-NLP-SG/LLM-R2`
- `https://arxiv.org/abs/2404.12872`

## Clues Found

Legacy LLM-R2 evidence includes:

- `llm_r2_pg9_bounded_evidence_reconciliation_v1.md`: PG9 original-route
  bounded evidence with 9 generated rows, 3 exact rows, and 6 execution-failed
  rows due malformed SQL.
- `llm_r2_recovered_extraction_pg6_bounded_evidence_review_v1.md`: PG6
  recovered-extraction route evidence, separate from original route.
- `llm_r2_supported_pg3_pg_execution_checker_review_v1.md`: PG3 checker-backed
  PostgreSQL evidence for `PERF_0006`, `PERF_0013`, and `PERF_0024`.
- `llm_r2_120_runner_recovery_inventory_v1.json` and
  `llm_r2_120_dependency_matrix_v1.csv`: runner, logical-plan substrate,
  output extraction, generated-SQL retention, and reproducibility blockers.
- retained run directories with recovered candidates, rule artifacts, prompt
  traces, and checker artifacts.

## Output Contract Clues

The legacy artifacts point to:

- complete SQL candidate files when extraction succeeds;
- raw `rewritten_sql_gpt` fields with extraction/truncation risks;
- rule activation metadata such as `activated_rules`;
- Java rule-applier markers in recovered-extraction paths;
- PG-only evidence and no recovered MySQL/Spark route.

## Use In This Task

These clues informed:

- fake rule-sequence metadata fields;
- rule-only response rejection;
- single-SQL extraction guards;
- explicit original-route versus recovered-route boundary language;
- future runtime placeholders for rule-system/checkpoint/demo-selector paths.

No legacy output was copied into current canonical metrics or user outputs.
