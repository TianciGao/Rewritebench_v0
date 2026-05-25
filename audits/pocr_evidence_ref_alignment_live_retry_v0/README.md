# POCR Evidence Ref Alignment Live Retry v0

This packet aligns the Stage A prompt evidence-ref instructions with the Stage B static evidence contract and records a bounded four-case live retry.

## Scope

- Fixture cases: PERF_0006, CONS_0005, PORT_0003, LONGTAIL_0011
- Candidate root: `runs/user/common_core_pg_noop_db_checker/candidate_sql`
- Live calls attempted: 4
- Provider label: `openai_compatible`
- Model label: `gpt-5.4`
- Schema-valid annotations: 4
- Malformed/schema-invalid annotations: 0
- Static validated operation atoms: 11
- Static rejected operation atoms: 0
- Insufficient-evidence atoms: 0

## Boundary

This is a bounded prompt/evidence-ref alignment retry only. It does not compute official Positive Operation Coverage Rate, aggregate route-level POCR, run DB/checker/timing, rerun a baseline, integrate with user output, or promote paper-facing metrics.
