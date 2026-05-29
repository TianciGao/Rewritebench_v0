# case_package_v2_witness_evidence_layers_pilot_v0

## Purpose and Scope

This branch-only writable pilot converted only the witness and evidence-reference layers for five v2 pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Previous writable pilots already converted manifest, SQL, schema, checker, and validation layers. This task did not convert metadata, notes, or runs; did not delete case-local evidence or case-local runs; did not run DB/checker execution; did not compute official metrics; did not update reports/results, denominators, paper results, case sets, inventory, or leaderboard outputs.

## Converted Layers

- Witness: each manifest now records the v2 source-as-oracle policy with `witness.mode: source_as_oracle`, `data_profile_status: external_or_generated`, and `correct_result_status: not_required_for_runtime_checker`.
- Witness profiles: each pilot case now has a lightweight `witness/witness_profile.yaml`.
- Evidence references: each manifest now has `evidence_ref` pointing to top-level `evidence/cases/<POOL>/<CASE_ID>/` paths.
- Evidence externalization: public-safe case-local evidence was copy-first externalized to top-level `evidence/cases/`.

## Cases Converted

All five pilot cases were converted for the witness and evidence-reference layers.

Cases deferred: none.

## Witness Policy Summary

The runtime checker oracle remains source-as-oracle. `correct_result.csv` was not fabricated for any case. `PERF_0006` retains its existing static `witness/correct_result.csv` and `witness/data_profile.yaml` as optional compatibility/static witness files; the other four cases use only the lightweight witness profile and source-as-oracle policy.

## Evidence Ref Summary

Each manifest now references:

- `evidence/cases/<POOL>/<CASE_ID>/package_validation_summary.json`
- `evidence/cases/<POOL>/<CASE_ID>/runs_retention.yaml`
- `evidence/cases/<POOL>/<CASE_ID>/retained_controls/`
- `evidence/cases/<POOL>/<CASE_ID>/hard_negative/`
- `evidence/cases/<POOL>/<CASE_ID>/plans/`
- `evidence/cases/<POOL>/<CASE_ID>/notes/`

Case-local `evidence/` remains in place as compatibility retained evidence. Compatibility pointers were recorded under `compatibility.evidence_legacy`.

## External Evidence Copy-first Summary

The following public-safe evidence groups were copied for each case:

- `package_validation_summary.json`
- `runs_retention.yaml`
- `retained_controls/`
- `hard_negative/`
- `retained_plans/` to external `plans/`

No raw unsafe evidence, prompt/API traces, credentials, or raw stdout/stderr/debug logs were copied. One retained flag mentioning stdout/stderr was preserved only as a false policy flag in `PORT_0003` runs-retention metadata.

## Case-local Evidence and Runs Preservation

Case-local `evidence/` was not deleted. Case-local `runs/` was not deleted. The only `runs/` files present in the five pilot cases remain placeholder `README.md` files.

## Protected Boundary Summary

- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.
- Metadata/notes/runs converted: no.
- Case-local evidence deleted: no.
- Case-local runs deleted: no.
- Legacy repo modified: no.

## Validation Summary

Static v2 validation passed for all five pilot cases. Unit tests under `tests/case_package_v2` passed. Summary JSON boundary assertions passed. `git diff --check` passed.

## Exact Next Safe Action

Authorize `case_package_v2_metadata_notes_runs_layers_pilot_v0` to handle only metadata, notes, and runs cleanup for the same five pilot cases, branch-only, with no DB/checker execution, evidence deletion without mapping, reports/results updates, denominator changes, paper-result changes, case_sets/inventory changes, official metrics, or leaderboard output.
