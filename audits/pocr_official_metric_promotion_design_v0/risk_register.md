# Risk Register

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Successful-subset bias from using only POCR@candidate | Missing candidates can make weak routes look strong. | Report POCR@planned first and POCR@candidate as a candidate-quality view. |
| Cherry-picking from POCR@curated without a frozen manifest | Curated subsets can be selected after outcomes are known. | Report POCR@curated as `NA` / `curated_manifest_missing` until a predeclared manifest exists. |
| Over-accept from span presence | No-op or source-like candidates could be credited. | Require Stage B transformation-aware validation and manual review no-op supported atoms. |
| Under-accept from overly conservative Stage B | True transformations may be rejected. | Track under-accept concentration and allow diagnostic manual review. |
| Annotation provider drift | Later annotations may not match earlier model behavior. | Record provider/model/prompt metadata and use checkpointed artifacts. |
| Malformed/provider failures | Missing or bad rows can hide coverage gaps. | Keep retry windows explicit and retain fail-closed rows after retry. |
| Route/candidate identity mismatch | Annotation could be applied to the wrong route or SQL. | Fail closed on case, engine, method, route, candidate SHA, or skills mismatch. |
| SQLGlot optimize missing candidate frontier | Full PG40 optimize annotation is blocked by missing candidates. | Keep missing optimize rows fail-closed for POCR@planned; do not substitute no-op candidates. |
| No-op substitution risk | Control outputs could be misused as optimize outputs. | Record route identity and candidate SHA; reject no-op substitution. |
| Confusion between POCR and correctness/speed metrics | POCR could be misread as exactness or speedup. | Report POCR beside RCR, GM, and denominator counts with scope notes. |
| Top-level reports/results pollution | Local diagnostic outputs could become paper-facing accidentally. | Keep D035 local output separate; require separate renderer authorization. |
| Accidental official promotion before gates | Diagnostic counts could be frozen prematurely. | Require D039 gates, manual review, and separate paper-facing authorization. |

POCR enters an official metric promotion process. This does not mean POCR is already an official paper metric.

Stage A annotation alone is not counted. Stage B transformation-aware validation is required. Semantic guard atoms are excluded from the operation coverage numerator and denominator.

No route-level POCR score is emitted in this task. No paper-facing metric is promoted in this task. No global leaderboard is produced.
