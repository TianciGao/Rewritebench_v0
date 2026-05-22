# Latest Paper Metric Scope

The decision records the latest-paper Table 6 target scope supplied for this task.

## Coverage

- Generation Rate: `|G_r| / N_S`
- Execution Coverage Rate: `|E_r| / N_S`

## Correctness

- Result Consistency Rate: `|X_r| / N_S`
- Semantic Equivalence Rate: `|V_equiv_r| / |V_equiv_r union V_non_r|`, with unknown/undecidable verifier outcomes reported separately

## Performance

- GM Speedup Ratio: `exp(|M_r|^-1 sum_{i in M_r} log s_i)`, where `s_i = t_src_i / t_rw_i`
- Speedup Ratio Percentiles: `P10`, `P25`, `P50`, `P75`, `P90` over `{s_i}_{i in M_r}`

Performance remains exact-gated and timed-gated. Timing artifacts must preserve paired source/candidate timing in the same engine, environment, and run context.

## Interpretability

- Positive Operation Coverage Rate: `|C_r|^-1 sum_{i in C_r} (|A_hat_i| / |A_exp_i|)`

POCR is deferred until operation atoms and validation schema are supplied by the collaborator's external script and reviewed.

## Generalization

- Cross-Engine Execution Coverage Rate: `|E_tgt_r| / N_PORT`
- Cross-Engine Result Consistency Rate: `|X_tgt_r| / N_PORT`
- Cross-Engine GM Speedup Ratio: `exp(|M_tgt_r|^-1 sum_{i in M_tgt_r} log s_tgt_i)`

## Delta From Older Repository Contract

The existing `repository_spec/metrics_contract_v1.md` remains present but reflects the older formalized contract:

- It includes Attribution Coverage.
- It includes Speedup Retention.
- It does not yet reflect POCR and Cross-Engine GM Speedup Ratio as latest-paper targets.

A future metrics contract delta/audit should reconcile these differences before implementation.
