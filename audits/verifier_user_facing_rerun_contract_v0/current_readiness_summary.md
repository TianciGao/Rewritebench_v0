# Current Readiness Summary

SQLSolver readiness:

- External SQLSolver setup and wrapper are available.
- SQLSolver layout/config contract is conformant.
- SQLGlot-noop PostgreSQL all-exact identity-guard diagnostic attempted 35 exact rows.
- Identity passed rows: 24/35.
- Corrected equivalent rows: 24.
- Corrected non-equivalent rows: 0.
- Corrected decidable rows: 24.
- Corrected local diagnostic SER: 1.0 over 24 corrected decidable rows.
- Corrected decidable coverage over exact rows: 24/35.

VeriEQL readiness:

- VeriEQL finite-bound wrapper is integrated.
- VeriEQL layout/config contract is conformant.
- SQLGlot-noop PostgreSQL identity-guard closeout checked 35 exact rows.
- Identity passed rows: 4/35.
- Corrected equivalent rows: 4.
- Corrected non-equivalent rows: 0.
- Corrected decidable rows: 4.
- Corrected local diagnostic SER: 1.0 over 4 corrected decidable rows.
- Corrected decidable coverage over exact rows: 4/35.

Readiness interpretation:

- SQLSolver is the stronger candidate for a future bounded verifier-support paper-facing policy packet.
- VeriEQL should remain bounded support evidence only unless coverage/identity limitations are addressed.
- Neither current diagnostic line is final paper evidence.
