# Large-Scale Experiment Plan

## Phase 0: Promotion Design Audit

This task is Phase 0. It records D039 and defines the promotion-process proposal. No experiments are run.

## Phase 1: Formula And Denominator Implementation

Implement POCR@planned and POCR@candidate according to the D039 denominator policy. No live API is used unless separately authorized. No paper-facing renderer is updated.

## Phase 2: Small Tri-Engine Pilot

Run a 5 cases x 3 engines x 2 routes pilot.

Routes:

- Direct LLM Repair-1
- SQLGlot no-op

Goals:

- Resolver stability
- Prompt dialect stability
- Stage B fail-closed behavior
- No-op over-accept check
- Route and candidate SHA binding

## Phase 3: PG40 Official Pilot

Main PG40 routes:

- Direct LLM original PG40
- Direct LLM + Repair-1 PG40
- SQLGlot no-op PG40
- SQLGlot optimize PG40 with missing rows fail-closed

Appendix or diagnostic PG40 routes:

- R-Bot adapted GPT-5.4 PG40
- LLM-R2 adapted GPT-5.4 PG40
- LearnedRewrite PG40 candidate-present rows plus missing fail-closed rows

PG40 must not be represented as Track A 120.

## Phase 4: Track A 120 Official POCR Expansion

Track A 120 is Common-core 40 x 3 engines = 120 planned rows.

Main routes:

- Direct LLM original
- Direct LLM + Repair-1
- SQLGlot no-op
- SQLGlot optimize
- Calcite HEP fail-closed

Candidate-present rows enter annotation. Missing candidate rows do not enter annotation and contribute zero to POCR@planned. Unsupported rows are retained with explicit status.

SQLGlot optimize missing rows must not be filled using no-op candidates.

If five routes run, the planned surface can reach 600 route-rows, but live annotation calls occur only on candidate-present rows. The process must be checkpointed, batched, and resumable.

## Phase 5: Quality Gate And Manual Review

Review route/candidate mismatches, no-op over-accept, schema-invalid rows after retry, under-accept concentration, and candidate identity binding.

## Phase 6: Paper-Facing Renderer And Freeze

Future paper-facing outputs, if separately authorized, should use explicit surfaces such as:

```text
reports/paper/pocr_official_metric_table_v0/
results/retained/pocr_official_metric_v0/
```

This requires separate authorization.

POCR@planned and POCR@candidate are the first two promotion views. POCR@curated is deferred until a predeclared curated manifest exists.

Stage A annotation alone is not counted. Stage B transformation-aware validation is required. Semantic guard atoms are excluded from the operation coverage numerator and denominator.

No route-level POCR score is emitted in this task. No paper-facing metric is promoted in this task. No global leaderboard is produced.
