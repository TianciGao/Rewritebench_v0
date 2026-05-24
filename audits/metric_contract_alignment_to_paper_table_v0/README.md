# Metric Contract Alignment To Paper Table

Task: `metric_contract_alignment_to_paper_table_v0`

Mode: audit/design only.

This packet aligns the latest paper metric table recorded in D032, the older repository metric contract in `repository_spec/metrics_contract_v1.md`, local diagnostic metric outputs in `src/sql_rewrite_bench/local_metrics.py`, diagnostic tag-slice outputs in `src/sql_rewrite_bench/tag_slices.py`, and verifier-phase Semantic Equivalence Rate support in `src/sql_rewrite_bench/verifier_support/`.

No source code, metric implementation, benchmark run, adapter run, DB/checker execution, timing run, LLM call, SQLSolver run, VeriEQL run, new metrics computation, official metric computation, paper report/result update, retained-evidence promotion, denominator change, case membership change, raw evidence change, env file, or secret change was performed.

Key findings:

- D032/latest paper table and D033/local metrics agree that local Result Consistency Rate is `exact / selected`, but `repository_spec/metrics_contract_v1.md` still defines Result Consistency Rate over executed candidate cases.
- D032/latest paper table uses POCR, while `metrics_contract_v1.md` uses Attribution Coverage; local metrics defer POCR and tag slices are not operation atoms.
- D032/latest paper table uses Cross-Engine GM Speedup Ratio, while `metrics_contract_v1.md` uses Speedup Retention; local metrics currently reports this as `N.A.` without target-engine paired timing.
- SER policy is conceptually aligned around formal verifier evidence only, but status vocabulary should be standardized before paper-facing promotion: `computed`, `coverage_limited`, or `N.A.`.
