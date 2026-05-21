# Readability Check

Public-facing Markdown files checked:

- `CONTRIBUTING.md`
- `benchmark_spec/README.md`
- `benchmark_spec/scope.md`
- `benchmark_spec/case_package_contract.md`
- `benchmark_spec/denominator_policy.md`
- `benchmark_spec/reporting_policy.md`
- `reports/README.md`
- `results/README.md`
- `docs/README.md`

Checks:

- Headings are on separate lines.
- Blank lines are present after headings.
- Bullet lists render as Markdown bullets.
- Code/path examples are wrapped in backticks.
- No compressed heading/body/table lines were found.
- No broken placeholder paths such as `cases///`, `runs/user//`, or `schemas//` were found.
- No internal migration, Codex, wave, or v2 language was found in the public-facing skeleton files.

Boundary wording preserved:

- Common-core v0 = 40 cases.
- Pool split = 16 PERF + 9 CONS + 9 PORT + 6 LONGTAIL.
- Track A same-engine denominator = 120 planned rows.
- Case package is the benchmark unit.
- Results are role-aware and denominator-aware.
- No global leaderboard.
- Hard negatives are checker controls.
- Verifier support is not a rewrite-generation baseline.
- `SpeedupTransferRate` is not computed for current evidence.
- User-entry outputs are local diagnostics, not official metrics.
- Reports/results are not updated by user-entry smoke or local diagnostics.
