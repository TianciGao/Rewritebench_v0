# Parser Contract

## Source Of Truth

D036 makes each Common-core root-level `skills.md` file the official future POCR operation-atom and semantic-guard contract:

```text
cases/<POOL>/<CASE_ID>/skills.md
```

The parser reads only this file for operation atoms and semantic guard atoms. It does not infer atoms from taxonomy tags, SQL text, positive SQL, negative SQL, candidate SQL, manifests, or retained evidence.

## Input

The parser accepts a `skills.md` path and reads it with `utf-8-sig`.

Required document features:

- `case_id` in the Scope section.
- `pool` in the Scope section.
- `## Atom Protocol` section.
- Markdown atom table with columns equivalent to:
  - `atom`
  - `category`
  - `type`
  - `risk`
  - `weight`
  - `requirement`
- `## Required Candidate Annotation Shape`.
- `## Review Boundaries`.

## Parsed Objects

The implementation exposes dataclasses:

- `SkillAtom`
- `SkillContract`
- `SkillParseResult`
- `SkillValidationIssue`

`SkillAtom` preserves normalized fields plus the raw table fields. Supported atom categories are:

- `operation_atom`
- `semantic_guard_atom`

Unknown categories are preserved as `unknown` and reported as validation issues.

## Inventory Helper

`build_common_core_inventory(repo_root)` reads `case_sets/common_core_v0/cases.csv`, validates the expected 40 Common-core case packages, and parses exactly those 40 root-level `skills.md` files.

Expected split:

- PERF: 16
- CONS: 9
- PORT: 9
- LONGTAIL: 6

`write_parse_only_report(inventory, output_dir)` writes audit-only CSVs. It is not a metrics writer and must not write user-run `output/`, top-level `reports/`, top-level `results/`, or case-local `runs/`.

## Explicit Non-Goals

- No API or LLM call.
- No API key access.
- No candidate SQL judging.
- No Stage A annotation.
- No Stage B evidence validation.
- No Positive Operation Coverage Rate computation.
- No official metrics or paper-facing promotion.
- No baseline rerun.
- No DB/checker/timing run.
