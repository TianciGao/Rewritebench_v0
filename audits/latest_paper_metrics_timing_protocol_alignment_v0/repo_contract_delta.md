# Repository Contract Delta

Baseline compared:

- `project_control/DECISION_LOG.md` D018
- `project_control/DECISION_LOG.md` D032
- `repository_spec/metrics_contract_v1.md`
- `repository_spec/metrics_contract_v1_draft.md`
- `repository_spec/explainability_attribution_policy_v1_draft.md`

## Delta Summary

| Area | Existing repository contract | Latest-paper/D032 target | Alignment recommendation |
|---|---|---|---|
| Interpretability | Attribution Coverage | Positive Operation Coverage Rate | Treat Attribution Coverage as historical; defer POCR until operation-atom schema is stable |
| Generalization performance | Speedup Retention | Cross-Engine GM Speedup Ratio | Replace retention framing with target-engine GM speedup over `M_tgt_r` |
| Regression@20 | Optional legacy diagnostic | Not in latest Table 6 scope | Keep diagnostic/open question only |
| Generation | Candidate emitted over planned denominator | `|G_r| / N_S` | Keep candidate emission distinct from preflight/readiness |
| Preflight/ready | Diagnostic fields | Not primary metric | Report separately, not in Generation Rate numerator |
| Execution coverage | "Attempted or completed" language in v1 needs policy | `|E_r| / N_S` | Prefer candidate execution success as numerator unless human confirms attempted-execution semantics |
| Result consistency | Existing v1 denominator is executed candidate cases | Latest formula uses `|X_r| / N_S` | Requires team confirmation whether Table 6 uses planned denominator or shorthand over eligible same-engine scope |
| Semantic equivalence | Verifier-decidable/result-consistent denominator | Latest formula uses decidable equivalent/non-equivalent set | Keep N.A. for no verifier evidence; report unknown/undecidable separately |
| Local diagnostics | User-entry local-only outputs exist | Not official metric inputs | Keep local outputs separate until retained-evidence/official promotion |

## Attribution Coverage vs POCR

The existing contract defines Attribution Coverage as a structured evidence coverage metric. D032 records that the latest paper uses Positive Operation Coverage Rate instead. POCR depends on expected operation atoms `A_exp_i` and matched/covered operation atoms `A_hat_i`, so it requires an external operation-atom schema and validation pathway.

Recommendation: do not mutate `metrics_contract_v1.md` in this task. Treat this audit as the delta input for a future contract update.

## Speedup Retention vs Cross-Engine GM Speedup Ratio

Speedup Retention in the existing contract requires paired source/target timing but leaves the formula unresolved. Latest-paper Cross-Engine GM Speedup Ratio gives an explicit target-engine geometric mean over `M_tgt_r`.

Recommendation: model cross-engine performance as its own target-engine metric with required target-engine source/reference timing and target candidate timing in the same run context.

## Regression@20

The existing contract demotes Regression@20 to optional legacy diagnostic. D032 keeps it as an open reporting question. This audit recommends retaining that stance until human/team confirmation.

## Denominator Concern

Latest-paper formulas for Execution Coverage Rate and Result Consistency Rate use `N_S`. Existing contract sometimes uses executed rows as correctness denominators. This is the highest-priority human confirmation item before implementation.
