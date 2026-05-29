# Repair-1 Fail-Closed Policy

Repair-1 should fail closed and produce no repaired candidate when any of these conditions occur:

- original Direct LLM candidate is missing
- original feedback payload is missing or malformed
- row is marked `unsupported_engine`
- live calls are not explicitly enabled for a live Repair-1 run
- provider key is missing for a live Repair-1 run
- provider request fails
- provider response is empty
- response contains no SQL candidate
- response contains multiple SQL candidates
- response contains multiple SQL statements
- extracted SQL fails preflight
- candidate execution fails
- checker mismatch remains after repair

The original Direct LLM route output remains immutable. Repair-1 must record its own bucket and status instead of editing original row status.
