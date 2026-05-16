# PORT_0008 Canonical Full Case Migration Pilot

Date: 2026-05-16

## Scope

This report records the one-case copy-first canonical-layout full case migration pilot for `PORT_0008`. It is not Common-core 40 migration, not batch migration, not DB validation, and not evidence regeneration.

## Why PORT_0008 After PORT_0004

`PORT_0004` completed the first full-case pilot in a legacy-compatible layout. `PORT_0008` is the first canonical-layout pilot and tests canonical package structure plus integration of previously validated sanitized Spark plan evidence.

## Legacy State Snapshot

- legacy pwd: `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`
- branch: `artifact/case-package-contract-alignment-clean`
- HEAD: `7e438b5d767922007a1ca456fed0bf2e237a8952`
- status: `## artifact/case-package-contract-alignment-clean...origin/artifact/case-package-contract-alignment-clean [behind 7]
 M reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_log_v1.txt
 M reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_plan_v1.md
 M reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_status_v1.csv
 M reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/reviewer_reproduction_log_v1.txt
 M reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py`
- diff name-status:

```text
M	reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_log_v1.txt
M	reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_plan_v1.md
M	reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/deterministic/deterministic_reproduction_status_v1.csv
M	reports/evaluation/common_core_v0/REVIEWER_REPRODUCTION_V1/reviewer_reproduction_log_v1.txt
M	reports/evaluation/common_core_v0/scripts/render_speedup_slice_summary_v1.py
```

- recent commits:

```text
7e438b5d docs: rewrite README for common-core reproducibility
6eefb7c2 docs: rewrite README for common-core reproducibility
c1cc0ff1 artifacts: add common-core reproduction input bundle
```

The dirty report files are pre-existing. This task did not alter the legacy repo.

## Copied File Groups

- SQL copied into `sql/`.
- DDL and witness load SQL copied into `schema/<engine>/`.
- Legacy validation scripts copied into `validation/` with output-policy caveat.
- Public-safe TSV and JSON retained evidence promoted into `evidence/`.
- Risk, witness, and checklist notes copied into `notes/`.

## Generated Metadata Files

Generated public-release metadata includes `manifest.yaml`, `README.md`, checker YAML, schema/data profiles, metadata YAML, hard-negative summary, package validation summary, migration notes, and full `evidence/runs_retention.yaml`.

## Sanitized Evidence Integration

Existing formal sanitized Spark plan files were reused unchanged:

- `cases/PORT/PORT_0008/evidence/retained_plans/rewrite_neg_01.sanitized.txt`
- `cases/PORT/PORT_0008/evidence/retained_plans/rewrite_pos_01.sanitized.txt`

Raw legacy Spark plan text files were not copied into public retained evidence. They remain mapped as do-not-delete originals through `evidence/runs_retention.yaml`.

## Validation Scripts Output Policy

The copied scripts in `validation/` are retained legacy validation assets. They were not executed during migration, are not yet canonical user runners, and future public runner outputs must not write to case-local `runs/` by default.

## Raw Runs Handling

Raw `runs/` was not copied wholesale. Public-safe retained evidence was promoted into `evidence/`; raw or non-public-safe run artifacts remain mapped only.

## Validator v0.2 Results

- Full-case validator result: PASS 1/1 for `PORT_0008`.
- Evidence-pilot regression result: PASS 6/6 for the six blocked-PORT evidence-pilot slices.

## Validation Summary

- SHA256 copy validation: PASS for 28 copied legacy files.
- Sanitized plan SHA validation: PASS for 2 reused sanitized Spark plan files.
- Public hygiene scan: PASS.
- YAML validation: PASS for 14 files.
- JSON validation: PASS for 7 files.
- Python compile: PASS.

## Claim Boundary

Denominator, paper results, Common-core membership, case admission status, route evidence, and benchmark claims were not changed. No leaderboard was introduced.

## Remaining Risks

- The copied validation scripts remain legacy assets and need a later user-runner policy pass before being presented as canonical execution entrypoints.
- Validator v0.2 checks structure and hygiene but does not yet enforce every canonical path semantic.
- Historical evidence-pilot files remain present for continuity and regression checks.
