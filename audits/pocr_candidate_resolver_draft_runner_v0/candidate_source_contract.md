# Candidate Source Contract

## Purpose

The resolver discovers existing candidate SQL artifacts for POCR diagnostics without running any method.

It is read-only. It does not create candidate SQL, rewrite SQL, execute SQL, run checkers, collect timing, call APIs, or compute POCR.

## Input

Required inputs:

- repository root;
- candidate root, such as `runs/user/common_core_pg_noop_db_checker/candidate_sql/`;
- `method_id`;
- `route_id`;
- engine label;
- optional Common-core case filter.

Candidate file naming convention for the current scaffold:

```text
<CASE_ID>__<engine>.sql
```

The scaffold is generic enough for later route-labeled candidate roots, but this dry-run only inspected the bounded PostgreSQL root above.

## Resolved Fields

The resolver emits:

- `case_id`
- `pool`
- `engine`
- `method_id`
- `route_id`
- `candidate_path`
- `candidate_present`
- `source_sql_path`
- `positive_sql_path`
- `negative_sql_path`
- `skills_md_path`
- `resolver_status`
- `boundary_notes`

## v2 Path Handling

The resolver uses current v2 case-local paths:

- `cases/<POOL>/<CASE_ID>/sql/source.sql`
- `cases/<POOL>/<CASE_ID>/sql/pos_01.sql`
- `cases/<POOL>/<CASE_ID>/sql/neg_01.sql`
- `cases/<POOL>/<CASE_ID>/skills.md`

Legacy names inside `skills.md` are aliases only and do not trigger file rewrites.

## Status Values

- `resolved`: source SQL, candidate SQL, and `skills.md` exist.
- `missing_candidate`: candidate SQL is absent.
- `missing_source_sql`: source SQL is absent.
- `missing_skills_md`: `skills.md` is absent.

The resolver does not infer operation atoms from candidate SQL or any other source. D036 remains the boundary: operation atoms and semantic guard atoms come from `skills.md` only.
