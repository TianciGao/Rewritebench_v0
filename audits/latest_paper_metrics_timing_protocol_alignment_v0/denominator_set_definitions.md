# Denominator Set Definitions

These are proposed definitions for latest-paper alignment. They are design definitions only and do not change repository denominators.

## Same-Engine Scope

`N_S`

The planned same-engine candidate denominator for a route/method/scope. For Common-core Track A same-engine this is expected to align with the approved same-engine planned case-engine rows, currently 40 cases x 3 engines = 120 planned rows for full tri-engine scope. Smaller route/engine/pool slices use the corresponding subset.

`G_r`

Rows in `N_S` for route `r` where the adapter/method emitted candidate SQL. Raw candidate emission counts here. Preflight, parser acceptance, readiness, and source-like/no-op are separate diagnostics.

`E_r`

Rows in `N_S` for route `r` where candidate execution succeeds under the approved engine execution protocol. Open question: whether attempted execution should count instead of successful candidate execution.

`X_r`

Rows in `N_S` for route `r` where candidate execution reaches checker comparison and result consistency is established under the approved checker/result protocol. Open question: whether latest paper intends planned denominator `N_S` or executed denominator for Result Consistency Rate.

`M_r`

Rows in `N_S` for route `r` that are result-consistent and have valid paired source/candidate timing in the same engine/environment/run context. This is the performance denominator for same-engine speedup.

`C_r`

Rows eligible for Positive Operation Coverage Rate for route `r`. This set must be versioned by operation-atom schema and validation stage. It is unavailable until external skill-adapter integration is reviewed.

## PORT / Generalization Scope

`N_PORT`

Approved PORT/generalization planned target-engine denominator. This must be role-aware and separate from Track A same-engine rows. Unsupported/fail-closed target roles remain visible.

`E_tgt_r`

Rows in `N_PORT` where target-engine candidate execution succeeds under the approved cross-engine route for route `r`.

`X_tgt_r`

Rows in `N_PORT` where target-engine result consistency is established under the approved cross-engine checking protocol.

`M_tgt_r`

Rows in `N_PORT` that are target-engine result-consistent and have valid paired target-engine source/reference and target-candidate timings in the same target engine/environment/run context.

## Invariants

- Denominator sets must be case-aware, engine-aware, route-aware, method-aware, and role-aware.
- Same-engine rows and PORT/generalization rows must not be merged.
- Controlled PORT target-reference diagnostics must remain separate from real adapter rows unless a future official protocol explicitly includes them.
- Unsupported/fail-closed rows must remain visible and must not be silently dropped.
