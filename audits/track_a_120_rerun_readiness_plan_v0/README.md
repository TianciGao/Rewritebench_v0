# track_a_120_rerun_readiness_plan_v0

Date: 2026-05-24

Mode: readiness/planning audit only.

This packet assesses readiness for a future Common-core v0 Track A same-engine
local diagnostic rerun:

- 40 Common-core cases
- 3 engines: PostgreSQL, MySQL, Spark
- 120 planned same-engine rows

No Track A 120 run, baseline run, SQL execution, timing, verifier row,
official metric computation, paper update, retained-evidence promotion,
leaderboard output, denominator change, or case membership change occurred.

## Top-line Readiness

- `sqlglot_noop`: ready for a first local diagnostic Track A 120 rerun, with known fail-visible PORT and label/frontier caveats.
- `sqlglot_optimize`: partially ready from bounded smoke only; blocked from direct 120 recommendation by known context-free `CONS_0005` invalid qualification.
- `calcite_hep_fail_closed`: PostgreSQL local diagnostic route card ready; MySQL/Spark/full-120 remain blocked by route-development blockers.
- `direct_llm_original`: blocked; needs user-facing adapter and prompt/model/provider/extraction metadata contract.
- `direct_llm_repair_1`: blocked; depends on Direct LLM original and repair-stage metadata contract.
- `sqlsolver`: support layer partially ready for PostgreSQL, but final candidate verifier rerun requires `sqlrb user verify --pair-scope run-candidates`.
- `verieql`: integrated but coverage-limited; keep as support evidence only.

## Recommended Next Safe Action

Authorize a SQLGlot noop Track A 120 local diagnostic rerun readiness prompt, or
first implement the verifier `run-candidates` facade if formal support evidence
is a prerequisite for the next phase.
