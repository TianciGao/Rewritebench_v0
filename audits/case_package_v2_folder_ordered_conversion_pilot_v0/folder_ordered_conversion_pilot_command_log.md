# Folder-ordered Conversion Pilot Command Log

Commands are summarized. No secrets, raw long outputs, DB/checker execution, metric computation, paper rendering, reports/results update, denominator change, evidence deletion, runs deletion, or leaderboard creation occurred.

## Preflight

- `pwd`: confirmed `/home/tianci_gao/code/Rewritebench_v0`.
- `git branch --show-current`: confirmed `feature/case-package-v2-external-schema`.
- `git remote -v`: reviewed origin.
- `git status -sb`: confirmed clean branch before edits.
- `git log --oneline -5`: reviewed recent branch commits.
- `git rev-list --left-right --count HEAD...origin/feature/case-package-v2-external-schema`: confirmed branch was not ahead or behind origin.

## Read-first Review

- Read project-control files, v2 specs, conversion rulebook, batch converter plan, folder-order refinement, and five pilot case packages.
- Reviewed current manifests, SQL paths, case-local schema files, external schema packages, and validator expectations.
- Confirmed the current validator still requires `schema_ref.engines`, while this task requires profile-first `schema_ref`.

## Conversion Actions

- Created direct `sql/pos_01.sql` and `sql/neg_01.sql` aliases for `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Verified existing direct SQL files for `PERF_0006`.
- Normalized the five manifests to canonical direct SQL references and profile-first `schema_ref`.
- Moved old SQL, schema, validation, checker-key, and miscellaneous manifest context into `compatibility` blocks where applicable.
- Normalized five case-local `schema/schema_profile.yaml` files to profile-only schema summary policy.
- Reused `schemas/tpch_common_core_v0/` for `PERF_0006`.
- Created copy-first external schema packages for `tpch_perf0007_v0`, `calcite_core_sql_tests_cons0005_v0`, `parrot_bird_port0003_v0`, and `sqlstorm_stackoverflow_longtail0011_v0`.
- Retained all old case-local schema engine files and nested SQL paths.

## Validation

- Manifest/SQL/schema sanity check: passed for all five cases.
- Protected later-layer directory check: passed; checker, validation, witness, evidence, metadata, notes, and runs directories were not modified.
- Protected repository surface check: passed; no `case_sets/`, inventory, reports, or results changes.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case <case>`: ran for all five cases and returned expected failures because the current validator requires `schema_ref.engines` and, for four cases, validation wrappers are out of scope.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: ran and failed only the existing `PERF_0006` read-only validation status assertion because profile-first `schema_ref` is not yet supported by the validator/test expectation.
- Summary JSON parse and boundary assertions: passed.
- Protected path checks for `case_sets/`, inventory, reports, results, evidence, and case-local runs: passed.
- `git diff --check`: passed.
- `git status -sb`: reviewed before explicit staging.
