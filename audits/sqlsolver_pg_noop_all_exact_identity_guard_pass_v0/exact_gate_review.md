# Exact Gate Review

Rows were eligible for SQLSolver only when all local source-run gates passed:

- selected by the source run;
- source executable;
- candidate generated;
- candidate executable;
- checker success;
- exact/result-consistent.

Gate result:

- 35 rows passed and were sent to SQLSolver.
- 5 rows failed and were recorded as `not_attempted_ineligible`: `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.

Local result-checker exactness was used only as an eligibility gate. It was not used as SQLSolver evidence and was not substituted for formal equivalence.
