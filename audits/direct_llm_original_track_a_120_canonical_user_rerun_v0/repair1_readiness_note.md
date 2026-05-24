# Repair-1 Readiness Note

Direct LLM original now has a canonical Track A 120 local diagnostic baseline:

```text
selected=120
candidate_generated=120
exact=102
mismatch=10
candidate_execution_failed=3
unsupported_engine=5
```

Repair-1 design is now better informed, but Repair-1 execution is not automatically authorized by this run.

Recommended prerequisites before Repair-1 execution:

1. Review the 18-row non-exact frontier.
2. Decide whether Repair-1 should target only extraction-valid candidate failures, only checker mismatches, or both.
3. Define prompt/metadata boundaries for repair attempts.
4. Add fail-closed accounting for repair attempts distinct from Direct LLM original.
5. Run a bounded Repair-1 smoke before any full Track A 120 repair route.
