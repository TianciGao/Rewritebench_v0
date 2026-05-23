# legacy_baseline_smoke_verifier_clue_audit_v0

## Verdict

Audit verdict: `completed_static_readiness_clues_found_no_new_verifier_evidence`.

The legacy folder `/home/tianci_gao/code/sql-rewrite-bench/reports/baseline_smoke/` contains two SQLSolver/VeriEQL readiness files:

- `reports/baseline_smoke/sqlsolver_verieql_support_readiness_v0.json`
- `reports/baseline_smoke/sqlsolver_verieql_support_readiness_execute_refused_v0.json`

Both are static support-readiness artifacts. They are not real VeriEQL execution output, not real SQLSolver execution output, not Semantic Equivalence Rate evidence, and not official metrics.

## Key Findings

- The readiness command was `baseline-smoke-sqlsolver-verieql-readiness` in legacy `scripts/cli.py`.
- The command intentionally refused execution when `--execute` was requested.
- Guardrails disabled SQLSolver, VeriEQL, SMT solver, database, SQLGlot, Calcite, LLM, dependency-install, artifact-download, and case-artifact writes.
- The readiness artifact selected nine PG-native candidates and classified one as `support_candidate`, six as `maybe`, and two as `exclude_from_first_support_scaffold`.
- `CONS_0007` was the only first support candidate because it is compact, Calcite-derived, verifier-style, and has source/positive/negative SQL plus schema material in the legacy repo.
- Adjacent legacy scratch notes contain useful clues for future bounded verifier work, including SQLSolver verdict mapping, VeriEQL JSONL pair shape, timeout-policy ideas, and constraint-bridge requirements.
- Those adjacent notes also include historical support evidence outside `reports/baseline_smoke/`; it must remain historical-only unless a separate retained-evidence mapping task authorizes reuse.

## Boundary

No legacy files were modified. No VeriEQL or SQLSolver tool was installed, copied, vendorized, or run. No Semantic Equivalence Rate, official metric, timing, speedup, retained evidence, top-level reports/results, paper table, or leaderboard output was computed or promoted.

## Next Safe Action

Use the audit only to guide a separately authorized bounded verifier path:

1. For VeriEQL, add a compatibility adapter for `SQLRB_VERIEQL_ROOT` that creates JSONL pair input and invokes `parallel.cli_within_timeout` from the VeriEQL root.
2. Start with fail-closed detection, then a one-case `CONS_0007`/`CONS_0035` canary only if dependencies and command paths are explicit.
3. For SQLSolver, keep external command-path reuse as the preferred mode; if a command or jar path becomes available, run only a bounded synthetic or `CONS_0007` smoke.
