# Sample User Output Tree

The integration smoke wrote to a temporary output root under `/tmp` and was not committed:

```text
/tmp/sqlrb_pocr_optional_user_run_integration_v0/output/
  logs/
    pocr_optional_user_run_sample_v0/
      pocr/
        pocr_diagnostic.log
  reports/
    pocr_optional_user_run_sample_v0/
      pocr_diagnostic.md
  results/
    pocr_optional_user_run_sample_v0/
      pocr/
        diagnostic_rows.csv
        diagnostic_summary_by_pool.csv
```

The equivalent D035 shape for a caller-provided local output root is:

```text
output/logs/<run_id>/pocr/pocr_diagnostic.log
output/reports/<run_id>/pocr_diagnostic.md
output/results/<run_id>/pocr/diagnostic_rows.csv
output/results/<run_id>/pocr/diagnostic_summary_by_pool.csv
```

No repository `output/`, top-level `reports/`, top-level `results/`, or `runs/` files were staged or committed.
