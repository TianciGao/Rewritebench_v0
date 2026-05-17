# retained_summary_adapter_v0

Developer-facing note. This is not public runner documentation and not a production retained-evidence adapter.

## Command

```bash
python scripts/dev/build_retained_summary_ledger.py \
  --out-dir audits/retained_summary_adapter_v0
```

## Scope

The adapter reads only curated release-repo summaries, Common-core scaffolds, inventory files, and repository specs. It refuses legacy paths and does not inspect legacy reports/results/runs.

## Outputs

- `audits/retained_summary_adapter_v0/retained_summary_ledger_v0.csv`
- `audits/retained_summary_adapter_v0/retained_summary_adapter_v0_summary.json`
- `audits/retained_summary_adapter_v0/retained_summary_adapter_v0_report.md`
- `audits/retained_summary_adapter_v0/retained_summary_adapter_v0_checks.csv`
- `audits/retained_summary_adapter_v0/retained_summary_adapter_v0_limitations.md`

## Non-goals

- No production retained evidence parsing.
- No legacy repo reads.
- No metrics computation.
- No reports/results migration.
- No production ledger under `results/retained`.
- No paper table rendering.

## Next Step

Review the audit output. Any adapter that parses real retained evidence or emits metric-eligible rows requires separate authorization.
