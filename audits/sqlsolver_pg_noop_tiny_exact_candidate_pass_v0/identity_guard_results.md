# Identity Guard Results

Identity sanity policy:

A source-vs-candidate row may enter the corrected decidable denominator only if:

- source-vs-source normalizes to `equivalent`;
- candidate-vs-candidate normalizes to `equivalent`;
- source-vs-candidate normalizes to `equivalent` or `non_equivalent`.

Results:

| Case ID | Source vs source | Candidate vs candidate | Source vs candidate | Identity guard | Corrected verdict |
|---|---|---|---|---|---|
| `CONS_0036` | equivalent | equivalent | equivalent | passed | equivalent |
| `CONS_0037` | equivalent | equivalent | equivalent | passed | equivalent |
| `LONGTAIL_0023` | equivalent | equivalent | equivalent | passed | equivalent |
| `PORT_0003` | unknown | unknown | unknown | failed | identity_guard_failed |
| `PORT_0005` | unknown | unknown | unknown | failed | identity_guard_failed |

Counts:

- Identity checked rows: 5.
- Identity passed rows: 3.
- Identity failed rows: 2.
- Corrected equivalent rows: 3.
- Corrected non-equivalent rows: 0.
- Corrected decidable rows: 3.
