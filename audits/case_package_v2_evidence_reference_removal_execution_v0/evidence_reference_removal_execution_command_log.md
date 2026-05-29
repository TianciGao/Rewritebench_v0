# Evidence Reference Removal Execution Command Log

- Repository preflight: confirmed `/home/tianci_gao/code/Rewritebench_v0`, branch `feature/case-package-v2-external-schema`, remote `origin`, and clean starting status.
- Read project-control files and prior evidence surface policy audit outputs.
- Inspected five pilot case packages and top-level static evidence directories.
- Confirmed case-local `evidence/` directories were already absent for all five pilot cases.
- Updated five manifests from `evidence_ref` to regeneration-first `evidence_policy`.
- Updated README evidence wording for all five pilot cases.
- Updated checker/witness YAML files that contained static evidence paths.
- Confirmed no live case refs to deleted five-pilot static evidence paths remained.
- Deleted five top-level static evidence directories under `evidence/cases/`.
- Ran static v2 validator for all five pilot cases: passed.
- Ran unit tests: `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed.
- Ran summary JSON assertion: passed.
- Ran protected-path diff check for `case_sets/`, `inventory/`, `reports/`, `results/`, `schemas/`, `scripts/dev/`, and `tests/case_package_v2/`: no unexpected changes.
- Ran `git diff --check`: passed.
- Ran `git status -sb`: reviewed changed paths before explicit staging.
