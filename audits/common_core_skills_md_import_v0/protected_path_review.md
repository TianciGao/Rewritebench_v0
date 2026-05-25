# Protected Path Review

This import was restricted to root-level `skills.md` files for the 40 Common-core case packages.

Allowed copied path shape:

```text
cases/<POOL>/<CASE_ID>/skills.md
```

Explicitly disallowed paths were not copied:

- `manifest.yaml`
- `README.md`
- `sql/`
- `schema/`
- `checker/`
- `validation/`
- `witness/`
- `evidence/`
- `runs/`
- `reports/`
- `results/`
- `output/`

The zip inventory found 40 selected root-level skills files and a full case-package archive surface. The import script copied only those 40 selected files after path traversal checks, separator normalization checks, Common-core membership matching, and content validation.

After import, the copied Markdown files were normalized from zip text line endings/trailing blank-line artifacts to repository LF style so that `git diff --check` passes. This normalization did not add or remove imported paths and did not copy any additional zip members.

Protected path result:

- imported files under `cases/`: 40
- imported non-`skills.md` files under `cases/`: 0
- `skill/` directories created: 0
- top-level `reports/` or `results/` updates: 0
- case-local `runs/` updates: 0
- `output/` updates: 0
- `cases.zip` staged: no

Validation commands confirmed:

- CSV parse checks passed for `zip_inventory.csv`, `imported_skills_inventory.csv`, and `skills_contract_validation.csv`.
- Common-core membership exact-match check passed for all 40 rows.
- Pool split check passed: PERF 16, CONS 9, PORT 9, LONGTAIL 6.
- Skills contract validation passed for all 40 imported files.
- `find cases -path '*/skill' -type d | wc -l` returned `0`.
- `find cases -path '*/skills.md' -type f | wc -l` returned `40`.
- Working-tree case path review found 40 changed case paths, all ending in `/skills.md`.
- `git diff --check` passed.
- Changed-file secret scan returned no findings.

This packet does not compute POCR and does not promote paper-facing metrics.
