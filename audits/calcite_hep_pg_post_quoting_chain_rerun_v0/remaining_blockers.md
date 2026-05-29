# Remaining Blockers

Remaining blocker categories:

- PORT no-candidate parse failures on double-quoted source identifiers: `PORT_0003`, `PORT_0005`, `PORT_0008`, `PORT_0012`.
- DATETIME/TIMESTAMP parse/type handling: `PORT_0004`, `PORT_0022`, `PORT_0025`.
- Schema-fallback policy exclusions: `PORT_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, `LONGTAIL_0024`.
- PORT PostgreSQL source-role failure: `PORT_0024`.
- Checker mismatch / semantic review: `PERF_0035`, `PERF_0062`, `CONS_0036`, `LONGTAIL_0011`, `LONGTAIL_0012`, `LONGTAIL_0013`.

Recommended separation:

- Do not combine DATETIME/TIMESTAMP hardening with PORT role-policy changes.
- Do not execute schema-fallback candidates by default until schema ingestion/fallback semantics are explicitly hardened.
- Review mismatch rows separately from generation/execution fixes.
