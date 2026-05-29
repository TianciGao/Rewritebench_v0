# Exact Gate Review

Verifier attempts were allowed only for rows satisfying all gates:

- selected
- source executable
- candidate generated
- candidate executable
- checker success
- exact/result-consistent

Gate result:

- Rows passing gate: 35
- Rows failing gate: 5
- VeriEQL attempted rows: 35
- `not_attempted_ineligible` rows: 5

The gate intentionally uses local result checker exactness only to decide whether a row may be sent to VeriEQL. It does not use local checker exactness as formal verifier evidence.

The full per-row gate and verifier outcome ledger is recorded in `per_row_verdicts.csv`.
