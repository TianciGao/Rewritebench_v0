# retained_summary_adapter_v0 Limitations

- This adapter only reads release-repo summary artifacts, case-set scaffolds, inventory files, and repository specs.
- It does not read legacy retained evidence.
- It does not parse production reports/results/runs.
- It does not compute metrics.
- It does not create official `results/retained` or `reports/evaluation` outputs.
- It emits only `retained_summary_artifact` rows.
- The output is not an official production evidence ledger and is not a metric input.
- Future adapters that parse retained evidence or emit metric-eligible rows need separate authorization.
