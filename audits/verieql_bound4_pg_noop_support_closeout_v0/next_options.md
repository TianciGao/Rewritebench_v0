# Next Options

Recommended path:

1. Start an independent SQLSolver setup/smoke/wrapper line.
2. Compare SQLSolver behavior on the four VeriEQL identity-passing rows and on `LONGTAIL_0023`.
3. Keep Semantic Equivalence Rate N.A. or coverage-limited until a verifier path has acceptable identity-pass and decidable coverage.

Alternative VeriEQL path:

- Stop broad VeriEQL expansion.
- Investigate identity failures by SQL feature class.
- Re-run identity guard only for a small targeted class after tool-support changes or policy clarifications.

Do not do next:

- Do not claim full Common-core SER from VeriEQL.
- Do not promote the corrected local rate into paper tables.
- Do not merge bound-4 and bound-10 evidence into one denominator.
- Do not treat local checker exactness as formal verifier equivalence.
