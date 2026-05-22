# Release-Surface Policy Decisions

Date: 2026-05-21

Purpose: record maintainer-approved policy decisions that govern the next release-surface metadata skeleton tasks. This file does not create public metadata files, implement metrics, render paper tables, update reports/results, create a release tag, or create an export branch.

## 1. License Decision

- Default public release license: `Apache-2.0`.
- Rationale: suitable for code/workbench repositories and includes an explicit patent grant.
- Scope note: use one repository-level `LICENSE` for the initial public release unless a later maintainer decision introduces dual licensing for data or documentation.
- Boundary: do not create the `LICENSE` file in this task.

## 2. Citation Decision

- Create `CITATION.cff` in a later metadata skeleton task.
- Use safe placeholder metadata until paper metadata is finalized.
- Project title: `SQL-RewriteBench`.
- Paper title may remain `TBD` or use `Beyond Faster SQL: Benchmarking Correctness, Observability, and Generalization in SQL Rewriting` if already approved by the maintainer.
- DOI must remain empty or `TBD` unless a final DOI exists.
- Author order and institutional metadata must not be invented by Codex.
- Boundary: do not create `CITATION.cff` in this task.

## 3. Contribution Policy Decision

- Create `CONTRIBUTING.md` in a later metadata skeleton task using a conservative policy.
- External contributions may propose documentation fixes, adapter examples, and issue reports.
- External contributions must not silently change Common-core membership, denominator definitions, official metrics, reports/results, retained evidence, case sets, or benchmark claims.
- New cases, metric changes, reports/results updates, and denominator changes require maintainer review and explicit policy approval.
- Boundary: do not create `CONTRIBUTING.md` in this task.

## 4. README Language Posture

- The current top-level README may remain Chinese on this construction branch.
- Before final VLDB/public artifact release, add an English README or adopt English as the primary public README with Chinese documentation retained separately.
- Boundary: do not rewrite `README.md` in this task.

## 5. benchmark_spec Scope Decision

- A later `benchmark_spec/` skeleton should cover public v0 scope only.
- It must preserve Common-core v0 = 40 cases.
- It must preserve pool split = 16 PERF + 9 CONS + 9 PORT + 6 LONGTAIL.
- It must preserve Track A same-engine denominator = 120 planned rows.
- It must state that the case package is the benchmark unit.
- It must require role-aware and denominator-aware reporting.
- It must preserve the no-global-leaderboard boundary.
- It must state that hard negatives are checker controls.
- It must state that `SpeedupTransferRate` is not computed for current evidence.
- It must state that verifier support is not a rewrite-generation baseline.
- Boundary: do not create `benchmark_spec/` in this task.

## 6. reports/results Boundary Decision

- Later create boundary README files for `reports/` and `results/`.
- User-entry outputs remain under `runs/user/{run_name}/`.
- User-entry local diagnostics do not update `reports/` or `results/`.
- Metadata skeleton tasks must not migrate or regenerate paper results.
- Boundary: do not create or modify `reports/` or `results/` in this task.

## 7. Release Branch/Tag Decision

- Do not create a release tag or export branch yet.
- Final export/release branch/tag should occur only after final public-release closeout passes.
- A possible future policy may use `release/v0-public` and `v0.1.0`, but these names are not created or reserved by this task.

## 8. Timing, Metrics, and Reproduction Boundary

- U8 timing diagnostic remains deferred unless a timing protocol is explicitly approved.
- Official metrics implementation remains unauthorized.
- Paper table rendering remains unauthorized.
- Retained-evidence adapter integration remains unauthorized unless separately approved.
- No global leaderboard is authorized.

## Next Safe Action

Authorize a metadata-only skeleton implementation task governed by these decisions, or collect any remaining maintainer metadata details before creating `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`, `benchmark_spec/`, `reports/README.md`, or `results/README.md`.
