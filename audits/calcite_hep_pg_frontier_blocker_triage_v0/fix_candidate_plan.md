# Fix Candidate Plan

Recommended authorization order:

1. `adapter_quoting_fix_candidate`

   Target rows: `PORT_0003`, `PORT_0005`, `PORT_0008`, `PORT_0012`, `CONS_0036`, `CONS_0037`, `LONGTAIL_0011`, `LONGTAIL_0012`, `LONGTAIL_0013`.

   Reason: this is the largest direct blocker class and affects both no-candidate parse failures and candidate execution failures.

2. `datetime_timestamp_mapping_fix_candidate`

   Target rows: `PORT_0004`, `PORT_0022`, `PORT_0025`, plus schema-fallback timestamp rows `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024` if schema ingestion hardening is authorized.

   Reason: DATETIME/TIMESTAMP handling blocks generation and fallback quality.

3. `port_role_scope_policy_needed`

   Target rows: `PORT_0013`, `PORT_0024`, and the broader PORT subset.

   Reason: PostgreSQL-only route interpretation should not accidentally execute non-PostgreSQL source-role SQL as if it were same-engine PostgreSQL.

4. `manual_case_review`

   Target rows: `PERF_0035`, `PERF_0062`, `CONS_0011`.

   Reason: these are result mismatches after successful source/candidate execution and need semantic review before any route interpretation.

Do not combine these into one broad runner change. Each fix should be separately authorized and followed by a bounded PostgreSQL rerun.
