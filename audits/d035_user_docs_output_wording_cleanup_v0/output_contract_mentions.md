# Output Contract Mentions

Validation target:

- User-facing docs must mention D035 exported output:
  - `output/results/<run_id>/`
  - `output/logs/<run_id>/`
  - `output/reports/<run_id>/`
- Mentions of `runs/user` must identify it as internal transitional staging or legacy/local staging, not the public output root.

Current status:

- `README.md`, `docs/README.md`, `docs/RUN_ARTIFACT_POLICY.md`, `docs/USER_ENTRY_DATA_FLOW.md`, `docs/USER_BENCHMARK_GUIDE.md`, `docs/LOCAL_ENGINE_SETUP.md`, `docs/guide/user_quickstart.md`, `docs/spec/output_contract.md`, `docs/spec/cli_contract.md`, `docs/templates/adapter_template.md`, `examples/README.md`, and `baselines/sqlglot/README.md` now use D035 output-root wording.
- `runs/user/<run_id>/` is described as internal staging before export.
- No user-facing doc is intended to present `runs/user/<run_id>/` as the primary user output root.

Official surfaces:

- Top-level `reports/` and top-level `results/` remain protected official/paper surfaces.
- Ordinary user-run tasks must not write there.
