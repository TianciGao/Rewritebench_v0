# Recommendation

## Wrapper And Schema Adjustment

No immediate wrapper input-format adjustment is required for the current `parallel.cli_within_timeout` JSONL path. The generated JSONL reaches VeriEQL and produces meaningful tool-native states.

Keep the current strict normalization policy:

- any `TMO` in the raw state list normalizes to `timeout`;
- `NEQ` normalizes to `non_equivalent`;
- `NSE` normalizes to `unsupported`;
- local result checker exactness is never substituted for verifier equivalence.

## Built-In Toy Smoke

If the team needs a clean local `equivalent` smoke for VeriEQL, authorize a separate task to add or exercise a finite-bound mode:

- prefer `parallel.cli_within_bound` for JSONL batch compatibility, or
- use VeriEQL's direct finite-bound API only as a clearly separate tool-behavior smoke.

The output must remain local-only and non-official.

## Stop Real-Case VeriEQL Expansion For Now

Do not expand real-case VeriEQL equivalent canaries based on `EQU+TMO`. The current real-case equivalent path has not produced clean decidable equivalence.

The only clean decidable timeout-mode path confirmed locally is non-equivalence (`NEQ`) for the synthetic `SELECT a FROM T` vs `SELECT b FROM T` pair.

## Proceed To SQLSolver Setup

Proceeding to SQLSolver setup or SQLSolver synthetic smoke is likely more productive if the immediate goal is verifier-support breadth. Keep VeriEQL available for fail-closed local diagnostics and future finite-bound toy experiments.

## Next Safe Action

Authorize one of:

1. A local-only finite-bound VeriEQL toy smoke using `parallel.cli_within_bound`.
2. SQLSolver environment setup and bounded synthetic smoke.
3. Pause verifier expansion and keep Semantic Equivalence Rate as `N.A.` until formal verifier evidence is cleanly available.
