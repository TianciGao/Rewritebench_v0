# Future Prompt Draft: case_package_v2_common_core_pilot_v0

You are working on SQL-RewriteBench clean public release migration / redevelopment.

Branch requirement:

- Work only on `feature/case-package-v2-external-schema`.
- Do not merge to `main`.
- Do not modify `case_sets/`, inventory, reports/results, denominators, paper results, retained evidence, or raw legacy evidence.

Task:

Expand the case-package v2 external-schema branch pilot to exactly these cases:

- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Use `PERF_0006` from `case_package_v2_external_schema_branch_pilot_v0` as the template.

Required scope:

- Copy SQL rewrites from nested positive/negative paths to direct `sql/pos_01.sql` and `sql/neg_01.sql` when present.
- Create or reuse external schema packages under `schemas/<SCHEMA_ID>/`.
- Add manifest `schema_ref` blocks.
- Create `witness/` profiles and correct-result material only when safely retained or derivable from existing public-safe retained outputs.
- Preserve case-local `runs/` as legacy retained evidence only.
- Do not delete case-local schema or runs directories during this expansion unless separately authorized.
- Do not run DB engines, checkers, timing workloads, LLM calls, or metric computation.

Validation:

- Static YAML parse for changed manifests and schema profiles.
- Static path checks for v2 SQL, witness, checker, validation, and schema_ref paths.
- Protected-boundary checks for `case_sets/`, inventory, reports/results, denominators, paper results, and retained evidence.
- Record any user-entry or validator compatibility gaps without patching broad runner behavior unless separately authorized.

Stop conditions:

- Any case outside the four listed cases changes.
- Any protected path changes.
- Any denominator, case membership, paper result, report/result, retained evidence, raw legacy evidence, metric, paper table, or leaderboard change.
- Any DB/checker/timing execution attempt.
- Any need to merge to main before pilot review.
