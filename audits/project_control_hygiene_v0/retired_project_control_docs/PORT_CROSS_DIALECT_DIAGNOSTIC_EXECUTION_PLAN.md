# PORT Cross-Dialect Diagnostic Execution Plan

## 1. Background

- The PostgreSQL Common-core local diagnostic run selected 40 rows and got 35 exact rows.
- Five PORT rows failed during source execution: `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Triage found MySQL-like `sql/source.sql` with backticks, MySQL functions, or MySQL-oriented types being executed directly by PostgreSQL.
- This is not a schema setup failure.
- This is not a rewriter-quality failure.
- This exposes a missing PORT cross-dialect diagnostic model in the current user-entry runner.

## 2. Current Limitation

Current same-engine local diagnostics assume:

- source query = `sql/source.sql`
- source engine = selected engine
- candidate query = adapter output
- candidate engine = selected engine

That assumption is valid for many same-engine cases. It is not valid for PORT cases whose `sql/source.sql` is source-engine dialect SQL, such as MySQL-like PARROT source SQL.

The current PostgreSQL diagnostic path therefore fails closed on MySQL-like source SQL before candidate execution and checker comparison.

## 3. Required Distinction

### Same-engine Local Diagnostic

- source query: `sql/source.sql`
- source engine: selected engine
- candidate query: adapter output
- candidate engine: selected engine
- checker compares same-engine source and candidate result artifacts

### PORT Cross-dialect Local Diagnostic

- source reference query: manifest-declared source-side query
- source reference engine: manifest-declared source engine, for example MySQL
- target candidate query: adapter output or approved target-side query
- target engine: selected target engine, for example PostgreSQL
- checker compares source-engine reference result artifact and target-engine candidate result artifact

These modes must not be silently mixed.

## 4. Manifest Role Metadata Policy

- The runner must not infer source, target, or reference roles from file names alone.
- The runner must not automatically treat `pos_01.sql` as a source oracle.
- The runner must not infer tags or roles from SQL text.
- PORT cross-dialect diagnostics require explicit manifest metadata.

Proposed additive metadata shape:

```yaml
local_diagnostic:
  modes:
    cross_dialect_reference:
      source_reference:
        engine: mysql
        query: sql/source.sql
      target_reference:
        engine: postgres
        positive_query: sql/pos_01.sql
      candidate_target:
        engine: postgres
```

Equivalent field names may be chosen in a later schema-design task, but the role semantics must be explicit.

- This metadata is additive.
- Existing PERF / CONS / LONGTAIL manifests without this metadata must continue using same-engine behavior.
- Missing or ambiguous metadata must fail closed.
- Adding metadata must not change Common-core membership, denominators, paper results, or official metrics.

## 5. Runner Policy

Future runner behavior:

1. Resolve case selection through `case_sets/`, unchanged.
2. Resolve case package normally.
3. If no cross-dialect diagnostic metadata exists, use same-engine local diagnostic behavior.
4. If explicit cross-dialect diagnostic metadata exists, resolve source reference engine/query from manifest.
5. Resolve target engine/query role from manifest and current adapter output.
6. Call the engine router for source-side and target-side execution.
7. Pass both result artifacts to the local checker.
8. If a required backend is not implemented or not configured, fail closed with explicit failure bucket/status.
9. Never silently fall back to another engine.
10. Never silently replace `source.sql` with `pos_01.sql`.

## 6. MySQL Execution Requirement

- To restore old-style PORT cross-dialect reference diagnostics for these five cases, MySQL source-side execution is required.
- MySQL execution is higher priority than Spark for this specific issue.
- MySQL backend should be implemented after manifest role metadata and runner policy are approved.
- MySQL backend must output the same kind of local JSONL result artifact expected by `local_result_checker.py`.
- MySQL backend must remain local diagnostic only.
- MySQL backend must not compute metrics, timing, reports/results, or leaderboard.

## 7. Spark Execution Status

- Spark execution is not required to resolve the five PostgreSQL PORT source failures.
- Spark remains future work unless a Spark source/target diagnostic use case is explicitly authorized.
- Spark backend must remain fail-closed until implemented.

## 8. Protection for Other Pools

- PERF / CONS / LONGTAIL behavior must be unchanged.
- Same-engine behavior remains default.
- Cross-dialect mode must be opt-in by manifest metadata.
- Regression tests must cover representative non-PORT cases:
  - `PERF_0006`
  - `CONS_0005`
  - `LONGTAIL_0011`
- Runner must not scan `cases/` to infer membership.
- Runner must not change `case_sets/`.
- No denominator or paper result changes.

## 9. Implementation Phases

### P0. Record This Plan and Decision

No code or case edits.

### P1. Manifest Role Metadata Design and Schema Check

Design exact manifest field names, validation expectations, and fail-closed behavior.

### P2. Add Explicit PORT Metadata

Add metadata only to selected PORT cases after P1 approval. No SQL edits.

### P3. Runner Metadata Consumption

Update resolver, runner, and engine router to consume explicit cross-dialect metadata. No guessing.

### P4. MySQL Execution Backend

Implement source-side MySQL local diagnostic execution. No timing, no official metrics.

### P5. Cross-dialect Checker Handoff

Ensure local checker can compare source-engine and target-engine result artifacts. Preserve normalization behavior.

### P6. PostgreSQL PORT Diagnostic Rerun

Rerun targeted five PORT cases and Common-core PostgreSQL diagnostic. Do not call results official metrics.

### P7. Spark Execution Backlog

Design or implement later only if explicitly authorized.

## 10. Acceptance Criteria

Stage is complete when:

- The five PORT case roles are explicit in manifests or policy.
- Runner does not guess roles.
- MySQL source-side execution can produce source reference artifacts for MySQL-like PORT source SQL.
- PostgreSQL target-side candidate execution can be compared to MySQL source reference artifacts.
- PERF / CONS / LONGTAIL same-engine behavior remains unchanged.
- Missing metadata or missing backend fails closed.
- Outputs remain under `runs/user/`.
- No official metrics, no paper results, no reports/results updates, no leaderboard.

## 11. Non-goals

- official metrics
- timing/speedup
- paper table rendering
- reports/results migration
- retained-evidence promotion
- release export/tag
- tag score/ranking
- changing Common-core membership
- changing denominators
- rewriting case SQL
