# Common-core 40 Migration Wave Plan

This is a future migration plan only. No migration was performed.

## wave_0_already_piloted: Completed representative pilots

Cases: `PERF_0006`, `CONS_0005`, `PORT_0004`, `PORT_0008`, `LONGTAIL_0011`

Why grouped: Use as regression/control only; do not remigrate.

Required preconditions: clean release repo; legacy read-only snapshot; explicit case list; no case-set updates; runs-retention mapping plan.

Codex autonomy level: high

Max batch size: 1

Expected duration: already complete

Validation gates: validator regressions stay green; public hygiene; YAML/JSON parse; py_compile; git diff/check/status.

Stop conditions: any pilot regression fails; dirty release repo; copied file hash mismatch; denominator/paper/membership change; raw legacy mutation; broad `git add .`.

Human approval needed: no

Exact next task recommendation: review only / regression baseline

## wave_1_low_risk_direct_canonical: Low-risk direct canonical

Cases: none currently assigned

Why grouped: Cases needing only straightforward canonical mapping and generated metadata.

Required preconditions: clean release repo; legacy read-only snapshot; explicit case list; no case-set updates; runs-retention mapping plan.

Codex autonomy level: high

Max batch size: 5

Expected duration: short

Validation gates: full-case + canonical-case + hygiene + SHA256; public hygiene; YAML/JSON parse; py_compile; git diff/check/status.

Stop conditions: any missing critical file or hygiene failure; dirty release repo; copied file hash mismatch; denominator/paper/membership change; raw legacy mutation; broad `git add .`.

Human approval needed: no

Exact next task recommendation: review only / regression baseline

## wave_2_sanitized_plan_needed: Sanitized Spark plan needed

Cases: `PERF_0007`, `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`, `PERF_0033`, `PERF_0034`, `PERF_0035`, `PERF_0052`, `PERF_0054`, `PERF_0056`, `PERF_0062`, `PERF_0077`, `PERF_0082`, `PORT_0003`, `PORT_0005`, `PORT_0012`, `PORT_0013`

Why grouped: Cases with public-safe controls but Spark plans/local paths requiring sanitized retained copies.

Required preconditions: clean release repo; legacy read-only snapshot; explicit case list; no case-set updates; runs-retention mapping plan.

Codex autonomy level: medium

Max batch size: 3

Expected duration: medium

Validation gates: sanitized plan scan, full-case, canonical-case; public hygiene; YAML/JSON parse; py_compile; git diff/check/status.

Stop conditions: raw local path remains in public files; dirty release repo; copied file hash mismatch; denominator/paper/membership change; raw legacy mutation; broad `git add .`.

Human approval needed: no if policy is already approved

Exact next task recommendation: prepare a future migration prompt for this wave and execute only after approval.

## wave_3_checker_hard_negative_approval_needed: Checker/hard-negative approval needed

Cases: `CONS_0007`, `CONS_0009`, `CONS_0010`, `CONS_0011`, `CONS_0012`, `CONS_0024`, `CONS_0036`, `CONS_0037`

Why grouped: CONS cases needing approved expected rejection semantics before migration.

Required preconditions: clean release repo; legacy read-only snapshot; explicit case list; no case-set updates; runs-retention mapping plan.

Codex autonomy level: low

Max batch size: 1

Expected duration: medium

Validation gates: checker metadata review, full-case, canonical-case; public hygiene; YAML/JSON parse; py_compile; git diff/check/status.

Stop conditions: expected rejection reason unclear; dirty release repo; copied file hash mismatch; denominator/paper/membership change; raw legacy mutation; broad `git add .`.

Human approval needed: yes

Exact next task recommendation: prepare a future migration prompt for this wave and execute only after approval.

## wave_4_complex_longtail_or_structure_review: Complex LONGTAIL/structure review

Cases: `LONGTAIL_0012`, `LONGTAIL_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, `LONGTAIL_0024`

Why grouped: LONGTAIL cases needing structural boundary and hard-negative review.

Required preconditions: clean release repo; legacy read-only snapshot; explicit case list; no case-set updates; runs-retention mapping plan.

Codex autonomy level: low

Max batch size: 1

Expected duration: medium

Validation gates: long-tail boundary review, full-case, canonical-case; public hygiene; YAML/JSON parse; py_compile; git diff/check/status.

Stop conditions: workload-frequency overclaim or unclear semantics; dirty release repo; copied file hash mismatch; denominator/paper/membership change; raw legacy mutation; broad `git add .`.

Human approval needed: yes

Exact next task recommendation: prepare a future migration prompt for this wave and execute only after approval.

## wave_5_reports_results_dependency: Reports/results dependency

Cases: none currently assigned

Why grouped: Cases blocked primarily by report/result evidence dependencies.

Required preconditions: clean release repo; legacy read-only snapshot; explicit case list; no case-set updates; runs-retention mapping plan.

Codex autonomy level: human_required

Max batch size: 1

Expected duration: variable

Validation gates: paper-boundary review; public hygiene; YAML/JSON parse; py_compile; git diff/check/status.

Stop conditions: paper result or denominator ambiguity; dirty release repo; copied file hash mismatch; denominator/paper/membership change; raw legacy mutation; broad `git add .`.

Human approval needed: yes

Exact next task recommendation: review only / regression baseline

## wave_6_defer_manual_review: Defer/manual review

Cases: `PORT_0022`, `PORT_0024`, `PORT_0025`

Why grouped: Cases with raw logs, prompt/token-like findings, or unresolved PORT evidence boundary.

Required preconditions: clean release repo; legacy read-only snapshot; explicit case list; no case-set updates; runs-retention mapping plan.

Codex autonomy level: human_required

Max batch size: 1

Expected duration: variable

Validation gates: manual review closeout before any migration; public hygiene; YAML/JSON parse; py_compile; git diff/check/status.

Stop conditions: any raw risky file cannot be mapped safely; dirty release repo; copied file hash mismatch; denominator/paper/membership change; raw legacy mutation; broad `git add .`.

Human approval needed: yes

Exact next task recommendation: prepare a future migration prompt for this wave and execute only after approval.
