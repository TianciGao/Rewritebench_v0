# Output Contract Review

D035 target user-facing output shape:

- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

Current D035-compliant implementation:

- `src/sql_rewrite_bench/user_output.py` implements `build_output_paths()`.
- `build_output_paths(Path("output"), "run_001")` resolves:
  - `output/results/run_001`
  - `output/logs/run_001`
  - `output/reports/run_001`
- `src/cli/main.py` uses `export_run_to_output()` after `sqlrb user evaluate`.
- verifier smoke helpers write under `output/results/<run_id>/verifier/`, `output/logs/<run_id>/`, and `output/reports/<run_id>/`.

Transitional source-run staging:

- `src/sql_rewrite_bench/user_run.py` still writes internal local source-run artifacts under `runs/user/<run_id>/`.
- `src/cli/main.py` currently invokes that internal runner and then exports to D035 output roots.
- This is a transitional implementation detail, not a paper or retained-evidence output surface.

Old-path findings:

- No committed source path was found that uses obsolete `output/<run_id>/...` as the user-facing output shape.
- Several docs still describe `runs/user/<run_id>/` as the user output root. These docs are outdated relative to the D035 facade/export contract and should be cleaned in a separate docs task.
- Baseline SQLGlot README still says outputs belong under `runs/user/<run_id>/`; this should be updated later to distinguish internal source-run staging from D035 exported user output.

Protected output surfaces:

- No top-level `reports/` or `results/` outputs are written by the current user-facing exporter.
- `user_output.py` rejects `reports` and `results` as output roots.
- User-run output must not be committed under `runs/user/`.

Verdict:

- User-facing output writer: D035-compliant.
- Internal staging: transitional and still `runs/user` based.
- Documentation: partial and needs D035 wording cleanup.
