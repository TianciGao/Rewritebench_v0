# Paper Table 6 Metric Extraction

Extraction source: D032 and task-provided latest-paper Table 6 context.

PDF status: `Beyond_Faster_SQL (5).pdf` was not found locally under `/home/tianci_gao`, `/mnt/data`, or `/tmp`. This extraction must be rechecked against the PDF when available.

## Coverage

- Generation Rate: `|G_r| / N_S`
- Execution Coverage Rate: `|E_r| / N_S`

## Correctness

- Result Consistency Rate: `|X_r| / N_S`
- Semantic Equivalence Rate: `|V_equiv_r| / |V_equiv_r union V_non_r|`

Unknown or undecidable verifier outcomes should be reported separately and should not be silently counted as equivalent or non-equivalent without a confirmed verifier policy.

## Performance

- GM Speedup Ratio: `exp(|M_r|^-1 sum_{i in M_r} log s_i)`, where `s_i = t_src_i / t_rw_i`
- Speedup Ratio Percentiles: `P10`, `P25`, `P50`, `P75`, `P90` over `{s_i}_{i in M_r}`

Performance is exact-gated and timed-gated.

## Interpretability

- Positive Operation Coverage Rate: `|C_r|^-1 sum_{i in C_r} (|A_hat_i| / |A_exp_i|)`

POCR is pending external skill-adapter integration and is not implementable from the current repository state.

## Generalization

- Cross-Engine Execution Coverage Rate: `|E_tgt_r| / N_PORT`
- Cross-Engine Result Consistency Rate: `|X_tgt_r| / N_PORT`
- Cross-Engine GM Speedup Ratio: `exp(|M_tgt_r|^-1 sum_{i in M_tgt_r} log s_tgt_i)`

Cross-engine metrics must use PORT/generalization denominator semantics and must not be merged with Track A same-engine rows.
