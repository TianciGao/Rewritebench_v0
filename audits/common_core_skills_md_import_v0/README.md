# Common-core Skills.md Import v0

This packet records a controlled case-local artifact import from:

`/home/tianci_gao/code/Rewritebench_v0/cases.zip`

Only root-level Common-core skill contract files were imported:

`cases/<POOL>/<CASE_ID>/skills.md`

No `skill/` directory was created. No other file from `cases.zip` was copied or overwritten.

## Import Result

- Imported `skills.md` count: 40
- Pool split: PERF 16, CONS 9, PORT 9, LONGTAIL 6
- Common-core membership match: exact match against `case_sets/common_core_v0/cases.csv`
- Existing destination conflicts: none
- Already-present identical files: none
- Imported Markdown files were normalized to repository LF text style after validation to satisfy `git diff --check`; no additional zip content was imported.

## Validation Summary

Every imported `skills.md` was validated as:

- readable as `utf-8-sig`
- case ID matches its destination directory
- pool matches its destination directory
- contains `Atom Protocol`
- contains at least one `operation_atom`
- contains at least one `semantic_guard_atom`
- contains `Required Candidate Annotation Shape`
- contains `Review Boundaries`

## Boundaries

- No Positive Operation Coverage Rate was computed.
- No live API call occurred.
- No DB/checker/timing run occurred.
- No baseline rerun occurred.
- No official metric promotion occurred.
- No denominator, case membership, paper result, or raw legacy evidence changed.
- `cases.zip` remains untracked and was not staged.

Next safe action: design a no-API POCR parser/adapter under `src/sql_rewrite_bench`, then connect the user-facing facade later.
