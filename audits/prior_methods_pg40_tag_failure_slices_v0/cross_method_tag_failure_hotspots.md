# Cross-Method Tag Failure Hotspots

This narrative is diagnostic only. It does not rank methods, does not compute primary metrics, and does not convert PG40 evidence into Track A 120 evidence.

## LearnedRewrite Failure-Tag Profile

LearnedRewrite has the broadest PG40 non-exact frontier: {'candidate_execution_failed': ['LONGTAIL_0011', 'LONGTAIL_0012', 'LONGTAIL_0013', 'LONGTAIL_0022', 'LONGTAIL_0023', 'LONGTAIL_0024'], 'fail_closed_no_candidate': ['CONS_0009', 'CONS_0012', 'CONS_0024', 'PERF_0035', 'PORT_0004', 'PORT_0008', 'PORT_0012', 'PORT_0013', 'PORT_0022', 'PORT_0024', 'PORT_0025'], 'mismatch': ['CONS_0005', 'CONS_0007', 'CONS_0010', 'CONS_0011', 'PERF_0019', 'PERF_0054']}. The fail-closed/no-candidate rows are concentrated in PORT and several CONS/PERF cases, while all six LONGTAIL rows are candidate-execution failures. The mismatch rows are in PERF/CONS cases and are associated with retained SQL-feature and rewrite-opportunity tags from the case manifests.

## R-Bot Failure-Tag Profile

R-Bot adapted GPT-5.4 has three non-exact PG40 rows: {'candidate_execution_failed': ['LONGTAIL_0011', 'PERF_0008'], 'mismatch': ['PORT_0013']}. `PORT_0013` is the mismatch row. `PERF_0008` and `LONGTAIL_0011` are candidate-execution failures. This is adapted local diagnostic behavior, not official R-Bot/RAG-stack behavior.

## LLM-R2 Failure-Tag Profile

LLM-R2 adapted GPT-5.4 has one non-exact PG40 row: {'candidate_execution_failed': ['LONGTAIL_0011']}. `LONGTAIL_0011` is the candidate-execution boundary. The official LLM-R2 runtime, checkpoint, demonstration selector, and Java rule-system were not used.

## Common PG40 Frontier Cases Across Methods

`LONGTAIL_0011` is the main cross-method repeated frontier. It is a candidate-execution failure for LearnedRewrite, R-Bot adapted GPT-5.4, and LLM-R2 adapted GPT-5.4.

## Tags Associated With Execution Failures

Execution failures include `LONGTAIL_0011` and, for LearnedRewrite, the remaining LONGTAIL cases. The repeated `LONGTAIL_0011` tag profile is: sql_feature=aggregate; sql_feature=cte; sql_feature=join; sql_feature=sort; sql_feature=window_function; rewrite_opportunity=cte_strategy; rewrite_opportunity=expression_simplification. These tags point to a complex CTE/window/join/aggregate/sort boundary, but this is only a diagnostic observation.

## Tags Associated With Mismatches

LearnedRewrite mismatches appear on `PERF_0019`, `PERF_0054`, `CONS_0005`, `CONS_0007`, `CONS_0010`, and `CONS_0011`. R-Bot has one mismatch, `PORT_0013`. LLM-R2 has no mismatch rows in PG40.

## Tags Associated With Fail-Closed/No-Candidate

Fail-closed/no-candidate rows occur only for LearnedRewrite in this PG40 evidence set: `PERF_0035`, `CONS_0009`, `CONS_0012`, `CONS_0024`, `PORT_0004`, `PORT_0008`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`. These rows indicate runtime/schema/request support boundaries rather than checker mismatches.

## Tags Associated With Source-Like/No-Op

Source-like/no-op diagnostics appear for LearnedRewrite on `CONS_0036` and `CONS_0037`, and for LLM-R2 adapted GPT-5.4 on `CONS_0037`. R-Bot has no source-like rows in the PG40 rerun audit. Source-like classification is not POCR and not a ranking metric.

## What Cannot Be Claimed

This packet cannot claim official metrics, official SER, POCR, paper results, retained evidence promotion, Track A 120 performance, or global method ranking. Failure bucket by tag is a diagnostic/support view only.
