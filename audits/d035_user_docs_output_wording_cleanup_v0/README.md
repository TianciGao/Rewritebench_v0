# d035_user_docs_output_wording_cleanup_v0

Date: 2026-05-24

Mode: documentation/layout hygiene only.

This packet records the D035 user documentation skeleton and output-wording
cleanup. It distinguishes user-facing exported output from internal
transitional staging:

- user-facing export: `output/results/<run_id>/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`
- internal staging: `runs/user/<run_id>/`
- official/paper surfaces: top-level `reports/` and top-level `results/`

No benchmark data, case sets, schemas, inventory files, scripts, source code,
tests, reports/results, retained evidence, runtime artifacts, metrics, or
experiment outputs were moved or regenerated.

## Conclusions

- D035 docs skeleton created under `docs/guide/`, `docs/spec/`, and `docs/templates/`.
- Existing user-facing docs and SQLGlot baseline README no longer describe `runs/user/<run_id>/` as the primary public output root.
- `runs/user/<run_id>/` is documented as internal transitional staging before D035 export.
- Physical migration to the final public `benchmarks/` target remains deferred.
- Paper/report/result surfaces remain protected.
