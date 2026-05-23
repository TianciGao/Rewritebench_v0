# Semantic Equivalence Rate Readiness

## Finite-Bound Mode Status

Finite-bound mode is viable for clean local toy verifier evidence:

- clean bounded `EQU`: yes
- clean `NEQ`: yes
- timeout-mode blocker isolated: yes

## Wrapper Readiness

The next implementation should not run exact candidates immediately. It should first add a finite-bound VeriEQL wrapper mode with:

- `parallel.cli_within_bound` command construction;
- explicit max-bound and per-bound timeout metadata;
- uppercase schema identifier canonicalization;
- raw output retention under local `output/results/<run_id>/verifier/`;
- local-only boundary flags;
- strict verdict normalization.

## Exact-Candidate Readiness

Not ready yet for exact-candidate local verifier pass. The tool path is promising, but schema canonicalization and finite-bound wrapper integration need implementation and tests first.

## Semantic Equivalence Rate Policy

Semantic Equivalence Rate remains `N.A.` for SQL-RewriteBench until formal verifier evidence exists for real exact-candidate rows. Synthetic toy evidence must not enter:

- Common-core evidence;
- official metrics;
- paper results;
- retained evidence;
- leaderboard output.

## Recommended Next Safe Action

Choose option B before option A:

1. Implement finite-bound VeriEQL wrapper mode and schema canonicalization.
2. Add regression tests using the two synthetic pairs from this probe.
3. Then separately authorize a tiny exact-candidate local verifier pass.
