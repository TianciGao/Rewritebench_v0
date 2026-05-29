# Source Docs Review

Reviewed source docs and README surfaces:

- `README.md`
- `docs/README.md`
- `docs/RUN_ARTIFACT_POLICY.md`
- `docs/USER_ENTRY_DATA_FLOW.md`
- `docs/USER_BENCHMARK_GUIDE.md`
- `docs/LOCAL_ENGINE_SETUP.md`
- `baselines/sqlglot/README.md`
- `baselines/calcite_hep_fail_closed/README.md`
- `examples/`
- prior inventory packet `audits/user_surface_d035_layout_inventory_v0/`

Pre-cleanup issue:

- Several user-facing docs described `runs/user/<run_id>/` as the user output root.
- The D035 skeleton directories `docs/guide/`, `docs/spec/`, and `docs/templates/` were absent.
- The docs did not consistently distinguish public exported output from internal source-run staging.

Docs already consistent:

- `src/sql_rewrite_bench/user_output.py` is D035-shaped and exports to `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`.
- `baselines/calcite_hep_fail_closed/README.md` already routes through `python -m cli.main user evaluate` and did not describe `runs/user/<run_id>/` as the public root.
