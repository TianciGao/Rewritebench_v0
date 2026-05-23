# Cross-Verifier Comparison

This comparison is diagnostic only. It does not declare either verifier universally correct.

| Case ID | VeriEQL status | SQLSolver tiny-pass status |
|---|---|---|
| `CONS_0036` | identity-passed equivalent | identity-passed equivalent |
| `CONS_0037` | identity-passed equivalent | identity-passed equivalent |
| `LONGTAIL_0023` | identity/modeling failure; not candidate drift | identity-passed equivalent |
| `PORT_0003` | identity-passed equivalent | identity failed with `UNKNOWN` on identity and source-candidate pairs |
| `PORT_0005` | identity-passed equivalent | identity failed with `UNKNOWN` on identity and source-candidate pairs |

LONGTAIL_0023 result:

- VeriEQL previously returned non-equivalent even for identity checks, so that row was classified as a VeriEQL identity/modeling diagnostic artifact.
- SQLSolver returned `EQ` for source-vs-source, candidate-vs-candidate, and source-vs-candidate.
- This supports the prior conclusion that the SQLGlot-noop candidate is not shown to have semantic drift by the available local evidence.

PORT result:

- SQLSolver returned `UNKNOWN` for `PORT_0003` and `PORT_0005` identity checks, so both are excluded from corrected SQLSolver `V_equiv`/`V_non`.
