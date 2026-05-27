# Source Positive Skills Role Review

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

Expected case-package locations reviewed:

- Source SQL path pattern: `cases/<POOL>/<CASE_ID>/sql/source.sql`
- Positive SQL path pattern: `cases/<POOL>/<CASE_ID>/sql/pos_01.sql`
- Optional negative SQL path pattern: `cases/<POOL>/<CASE_ID>/sql/neg_01.sql`
- Skills contract path pattern: `cases/<POOL>/<CASE_ID>/skills.md`

Implementation review:

- `src/sql_rewrite_bench/pocr/candidate_resolver.py` resolves `source.sql`, `pos_01.sql`, `neg_01.sql`, `skills.md`, and candidate SQL as distinct paths.
- `src/sql_rewrite_bench/pocr/skills_parser.py` parses only the case-local root-level `skills.md` Atom Protocol table; it does not inspect source SQL, positive SQL, candidate SQL, taxonomy, runtime evidence, or retained evidence to infer atoms.
- `src/sql_rewrite_bench/pocr/user_facade.py` reads source SQL, candidate SQL, and positive SQL separately and passes them to Stage B. The expected operation atom count is `len(contract.operation_atoms)`, not derived from SQL text.
- `src/sql_rewrite_bench/pocr/operation_evidence_policy.py` uses positive SQL only during evidence validation/alignment for a declared atom.

Verdict: `pass`. source SQL and positive SQL are distinct evidence/context inputs; `skills.md` is the only operation-atom source.

Boundary retained: positive SQL is reference evidence, not an atom source. candidate/source/positive span presence alone is not operation support.
