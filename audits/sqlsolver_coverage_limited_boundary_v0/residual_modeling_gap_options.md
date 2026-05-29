# Residual Modeling Gap Options

## Option A: Stop here and mark SQLSolver coverage-limited for public v0

Risk: public v0 has no broad SQLSolver SER line.
Benefit: avoids overclaiming verifier evidence and preserves clean boundaries.
Repair-1 impact: does not block Repair-1, because SQLSolver limitations are not rewrite-method failures.
Recommendation: preferred short-term option.

## Option B: Future narrow schema-modeling fix for the three residual blockers

Risk: wrapper/schema fixes can become semantic rewrites if not tightly scoped and tested.
Benefit: may recover the same-8 stability gate and unlock a later 35-row PostgreSQL no-op pass.
Repair-1 impact: optional; should not block fake-provider Repair-1 implementation.
Recommendation: authorize only if verifier coverage is prioritized before Repair-1.

## Option C: Try VeriEQL later as separate coverage-limited support line

Risk: VeriEQL has its own feature limitations and may not cover these residual blockers.
Benefit: independent verifier-support signal without expanding SQLSolver prematurely.
Repair-1 impact: optional and separate.
Recommendation: keep separate from SQLSolver status and do not use it to paper over SQLSolver gaps.

## Option D: Do not use local checker exactness as substitute SER

Risk: none; this preserves metric correctness.
Benefit: avoids promoting result-consistency evidence into formal semantic proof.
Repair-1 impact: none.
Recommendation: mandatory boundary.
