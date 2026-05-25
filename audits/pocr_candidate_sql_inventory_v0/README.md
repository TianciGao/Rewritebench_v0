# POCR Candidate SQL Inventory v0

This packet records D038 and Step 1 of the accepted short-term POCR maturity roadmap: read-only inventory and preservation mapping for existing baseline candidate SQL assets under `runs/user/`.

Inventory scope:

- Candidate roots scanned: 1,660.
- Candidate files inventoried: 2,377.
- PG40-complete PostgreSQL roots: 5.
- Track-A-120-complete route-family component roots: 6.
- Ambiguous roots: 1,579, mostly unit-test and small smoke artifacts.

Created inventory files:

- `candidate_root_inventory.csv`
- `candidate_file_inventory.csv`
- `candidate_sha256_manifest.csv`

Key findings:

- Direct LLM original and Direct LLM Repair-1 have complete tri-engine candidate families and PG40-complete PostgreSQL roots.
- R-Bot adapted GPT-5.4 and LLM-R2 adapted GPT-5.4 have PG40-complete PostgreSQL prior-method candidate roots.
- SQLGlot no-op has a PG40-complete PostgreSQL control root at `runs/user/common_core_pg_noop_db_checker/candidate_sql/`; its canonical Track A root files are incomplete for PostgreSQL candidate SQL preservation.
- LearnedRewrite has 29 preserved PostgreSQL candidate files in the manual-inspection rerun root, matching generated candidates rather than all 40 selected rows.
- SQLGlot optimize and Calcite HEP canonical candidate roots are not PG40-complete as candidate-file preservation roots; fail-closed/no-candidate rows remain visible through prior audit metrics, not through candidate SQL files.

Recommended next route:

- Direct LLM Repair-1 PostgreSQL PG40 diagnostic annotation-generation plus user-facing replay, because `runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql/` is PG40 complete and its tri-engine family is complete.

Boundary:

- No candidate SQL was moved, copied, deleted, normalized, regenerated, or rewritten.
- No live API call, API key read, annotation JSONL generation, DB/checker/timing run, baseline rerun, official POCR computation, route-level POCR aggregation, paper-facing metric promotion, repository `output/` commit, top-level reports/results update, denominator change, case membership change, paper result change, raw legacy evidence change, or leaderboard output occurred.
