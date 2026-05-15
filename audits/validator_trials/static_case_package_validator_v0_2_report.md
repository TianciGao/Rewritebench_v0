# Static Case Package Validator v0.2 Trial Report

Date: 2026-05-15

## Scope

This report covers validator v0.2, which adds `full-case` mode to `scripts/dev/validate_case_package.py`.

This is a release-repo static validator enhancement only. It is not full case migration, not Common-core 40 migration, not evidence regeneration, and not DB validation.

## What Changed From v0.1

- Validator version advanced from `v0.1` to `v0.2`.
- Existing `evidence-pilot` mode was preserved and rerun as a regression check.
- New `full-case` mode was added for future copy-first full case migration pilots.
- New `--out` CSV output was added.
- New `--json-out` output was added; `--json-output` remains supported as a backward-compatible alias.
- New advisory behavior was added through `--allow-failures` and `--advisory`.
- YAML parsing now uses PyYAML when available and falls back to text-level checks if unavailable.

## Trial 1: Evidence-Pilot Regression

Command:

```bash
python scripts/dev/validate_case_package.py \
  --mode evidence-pilot \
  --case cases/PORT/PORT_0008 \
  --case cases/PORT/PORT_0012 \
  --case cases/PORT/PORT_0013 \
  --case cases/PORT/PORT_0022 \
  --case cases/PORT/PORT_0025 \
  --case cases/PORT/PORT_0024 \
  --out audits/validator_trials/evidence_pilot_regression_results.csv
```

Result: pass, 6 of 6 cases passed.

Output:

- `audits/validator_trials/evidence_pilot_regression_results.csv`

## Trial 2: Full-Case Advisory Dry Run

Command:

```bash
python scripts/dev/validate_case_package.py \
  --mode full-case \
  --allow-failures \
  --case cases/PORT/PORT_0008 \
  --case cases/PORT/PORT_0012 \
  --case cases/PORT/PORT_0013 \
  --case cases/PORT/PORT_0022 \
  --case cases/PORT/PORT_0025 \
  --case cases/PORT/PORT_0024 \
  --out audits/validator_trials/full_case_mode_advisory_results.csv
```

Result: advisory expected-fail, 0 of 6 cases passed full-case mode.

The failures are expected because the current six slices are evidence-mapping pilots only, not complete migrated case packages.

Expected missing components detected for each case:

- `manifest.yaml`
- source SQL
- positive rewrite SQL
- hard negative or manifest-declared hard-negative not-applicable reason
- schema/data context
- checker or normalization config
- validation path
- provenance
- taxonomy

The validator also recognized that the existing evidence mapping is present:

- `evidence/runs_retention.yaml` exists and parses.
- Sanitized public evidence scans pass.
- No raw local path claims were found.
- Denominator and paper-result change claims remain absent.
- Formal evidence mapping checks remain satisfied.

Output:

- `audits/validator_trials/full_case_mode_advisory_results.csv`

## Trial 3: Command Sanity

Command:

```bash
python -m py_compile scripts/dev/validate_case_package.py
```

Result: passed.

## Boundary Confirmation

- Legacy repository modified: no.
- Raw legacy evidence changed: no.
- Full case migration started: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.

## How This Prepares The Next Pilot

The new `full-case` mode gives a reusable static gate before migrating a complete case package. It can be run in strict mode once a copy-first full package exists, and in advisory mode while building a candidate package.

For the next migration pilot:

- `PORT_0004` is lower risk because it avoids the sanitized Spark plan complication.
- `PORT_0008` is useful after that or instead if the goal is to test full migration plus already-realized sanitized retained evidence.

## Next Safe Action

Choose the first copy-first full case migration pilot, preferably `PORT_0004` for lower risk or `PORT_0008` to test sanitized evidence integration, and run validator v0.2 in advisory mode while assembling the candidate package.
