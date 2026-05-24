# Metrics Contract D032/D033 Patch

Task: `metrics_contract_d032_d033_patch_v0`

The repository metric contract was updated in place: `repository_spec/metrics_contract_v1.md`.

This patch aligns the contract with D032/latest paper table names and D033 local metric formulas. It corrects canonical Result Consistency Rate to `exact / selected`, preserves D033 Generation and Execution Coverage formulas, defines verifier-phase SER policy, marks POCR as paper-facing but deferred, replaces old Speedup Retention wording with Cross-Engine GM Speedup Ratio, and keeps failure buckets/tag slices diagnostic only.

No code or experiment was run. No adapters, DB execution, checker, timing, LLM, SQLSolver, VeriEQL, local metric recomputation, official metric computation, paper table rendering, reports/results update, retained-evidence promotion, denominator change, case membership change, raw legacy evidence change, env file, API key, or secret change occurred.
