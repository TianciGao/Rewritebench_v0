# Contract Patch Summary

## Result Consistency Denominator

`repository_spec/metrics_contract_v1.md` now defines canonical Result Consistency Rate as:

```text
Result Consistency Rate = exact / selected
Paper notation = |X_r| / N_S
```

The executed-candidate denominator is no longer canonical. An executed-subset consistency view may exist only as a separately named diagnostic and must not replace canonical Result Consistency Rate. This matches current D033 local diagnostic behavior in `src/sql_rewrite_bench/local_metrics.py`.

## SER / Verifier Phase

SER remains a primary correctness metric, computed only from formal verifier evidence:

```text
SER = |V_equiv| / |V_equiv union V_non|
```

Source-vs-candidate verifier pairs are limited to exact/result-consistent rows. Local result-checker exactness is explicitly forbidden as SER evidence. Unknown, timeout, unsupported, not_implemented, tool_error, no_verifier_support, and not_attempted outcomes are excluded from the decidable SER denominator and reported separately. SQLSolver and VeriEQL are verifier/support tools, not rewrite baselines.

## POCR Deferred

Positive Operation Coverage Rate is now the paper-facing interpretability metric. It remains deferred until a separately authorized external collaborator operation-atom/skill-adapter task provides stable evidence. The contract forbids creating skill folders, operation atom files, or inferring operation atoms from tags, SQL text, positive SQL, manifest prose, README text, checker files, failure buckets, tag_slices, or plan deltas.

## Cross-Engine Naming

The contract now uses the latest-paper generalization names:

- Cross-Engine Execution Coverage Rate
- Cross-Engine Result Consistency Rate
- Cross-Engine GM Speedup Ratio

Old Speedup Retention wording is marked historical/superseded. Track A same-engine timing must not be reused as Track C transfer-speed evidence.

## Failure / Tag Diagnostic Boundary

Failure buckets and tag_slices remain diagnostic/support only. They are not primary metrics, ranking scores, leaderboard inputs, or POCR substitutes.

## Local vs Official Boundary

`local_metrics.py` outputs remain non-official local diagnostic metrics. They must not update top-level reports/results, promote retained evidence, render paper tables, create a leaderboard, or change denominators, case membership, paper results, retained evidence, or raw legacy evidence.
