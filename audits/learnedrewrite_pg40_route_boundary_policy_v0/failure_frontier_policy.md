# Failure Frontier Policy

Source packet: `audits/learnedrewrite_pg40_bounded_local_diagnostic_v0/`.

Final PG40 frontier:

| Bucket | Count | Boundary interpretation |
| --- | ---: | --- |
| exact | 17 | Candidate generated, candidate executed, checker exact, and exact rows were timing-eligible/timed. |
| mismatch | 6 | Candidate generated and executed, but local checker did not find exact/result-consistent output. This is result-consistency failure evidence for PG40 local diagnostics only. |
| candidate_execution_failed | 6 | Candidate generated and passed preflight, source execution succeeded, but candidate SQL failed PostgreSQL execution. This is a generated-SQL execution/runtime compatibility boundary. |
| fail-closed/no-candidate | 11 | External runtime returned `status=false` / `Get Error`; no candidate SQL was emitted, extraction was not attempted, and DB/checker/timing were skipped. This is a runtime/schema/request support boundary. |

Boundary rules:

- Fail-closed/no-candidate rows remain visible in the PG40 selected denominator.
- Candidate execution failures remain visible in the PG40 selected denominator and do not become checker mismatches.
- Checker mismatches remain visible as non-exact rows and are not eligible for speedup interpretation.
- Exact rows may support local diagnostic timing summaries only when timed.
- No failure bucket here is a package hard-negative control.
- No failure bucket here is POCR, SER, or a leaderboard input.

Rows in the fail-closed/no-candidate frontier should be triaged before any broader LearnedRewrite route is considered. Rows in the candidate-execution-failed frontier require generated-SQL execution/dialect/runtime analysis before broader claims.
