# Checker Label Policy Design

Verdict: `design_ready_for_separately_authorized_patch`.

This design follows `mysql_label_policy_triage_v0`, which confirmed five MySQL SQLGlot noop rows where source and candidate values matched positionally and only result-column labels differed:

- `PERF_0062`
- `PORT_0004`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`

This packet is design/audit only. It does not change `local_result_checker.py`, checker configs, case packages, SQLGlot adapters, exact counts, reports/results, retained evidence, official metrics, timing/speedup, or leaderboard outputs.

## Current Behavior

The same-engine checker path reads result JSONL rows as dictionaries, normalizes values while preserving dictionary keys, and compares the full normalized source and candidate row lists with `normalized_source == normalized_candidate`.

Column labels are therefore part of exactness implicitly because they are JSON object keys. There is no explicit same-engine label policy in `compare_config.yaml` or `normalization.yaml`.

Cross-dialect controlled diagnostics already use a separate role-gated positional value comparison when manifest metadata enables cross-dialect normalization. That path does not represent a global label policy.

## Proposed Policy

Recommended first patch, if authorized later:

- Keep `exact_status` strict by default.
- Add diagnostic visibility for label-only mismatches: `value_exact`, `label_exact`, and `label_only_mismatch` in checker details and mismatch artifacts.
- Do not convert label-only mismatches into exact rows unless a separate explicit policy is added later.
- Do not globally ignore labels.
- Keep explicit aliases strict by default.
- Treat generated expression labels as eligible for warning/diagnostic classification only; do not infer that they are safe to ignore from result labels alone.

Possible later opt-in policy:

```yaml
result_comparison:
  column_label_policy:
    label_policy: strict
```

Supported policy names should start with:

- `strict`: default; labels are part of exactness.
- `diagnose_label_only`: labels remain strict, but label-only mismatches are surfaced explicitly.
- `positional_values_only`: explicitly authorized per case/role only; row and column counts plus positional values decide exactness, with label differences retained as warnings.

`ignore_generated_expression_labels` should not be implemented unless the checker receives explicit alias/provenance metadata or the case config explicitly declares that generated labels are non-semantic.

## Recommendation

Implement `diagnose_label_only` first as behavior-preserving infrastructure. Consider any label-relaxing mode only after a separate patch task defines config ownership, migration expectations, and regression coverage.

## Boundary

This is local diagnostic design only. It is not official metric design, not paper-results migration, not retained-evidence promotion, not timing/speedup work, and not a leaderboard.

## Validation

- Project-control readability check: passed.
- Audit Markdown sanity check: passed.
- `git diff --check`: passed.
- Protected-surface status check: passed.
- `runs/user/` committed-output check: passed.
