# Track A Rerun Sequence Recommendation

Recommended ordered sequence:

1. Run SQLGlot noop Track A 120 as a local diagnostic D035 rerun.
   - Rationale: route-specific adapter is under `baselines/`, CLI access works through `sqlrb user evaluate`, tri-engine local diagnostic evidence exists, timing and local metrics projection are implemented, and known frontiers are fail-visible.
   - Boundary: not official metrics, not paper-facing, no leaderboard.

2. Refresh SQLGlot optimize through bounded D035 diagnostics before any 120-row attempt.
   - Rationale: the context-free optimize route has a known `CONS_0005` invalid qualification failure on all engines.
   - Decision point: keep context-free route fail-visible or design a separately named schema-aware route.

3. Keep Calcite HEP at PostgreSQL-only readiness until blocker classes are addressed.
   - Rationale: PostgreSQL route card is refreshed after the quoting fix, but MySQL/Spark are not validated and blocker classes remain: no-candidate rows, DATETIME/TIMESTAMP, PORT source-role, schema-fallback policy, and mismatches.

4. Implement a user-facing verifier rerun facade before any final SER work.
   - Required shape: `sqlrb user verify --pair-scope run-candidates`.
   - Required policy: exact/result-consistency gate plus source-vs-source and candidate-vs-candidate identity guard.
   - Preferred verifier: SQLSolver first, because PG noop evidence is stronger than VeriEQL.

5. Defer Direct LLM original until deterministic routes and verifier facade are stable.
   - Required before run: provider/model contract, prompt versioning, extraction metadata, output schema, and reproducibility boundaries.

6. Defer Direct LLM Repair-1 until Direct LLM original is ready.
   - Required before run: repair-stage metadata, execution-feedback contract, and separation of original vs repaired candidate rows.

7. Prepare a final paper-facing rerun authorization packet only after local diagnostic reruns and verifier facade are stable.
   - This packet must explicitly authorize any official metric computation, paper table rendering, retained evidence promotion, or top-level `reports/` / `results/` update.

Unauthorized in the next step:

- Track A paper-facing run.
- Official metrics.
- Formal Regression@20.
- Semantic Equivalence Rate without verifier identity guard.
- Leaderboard output.
- Retained-evidence promotion.
- Physical layout migration.
