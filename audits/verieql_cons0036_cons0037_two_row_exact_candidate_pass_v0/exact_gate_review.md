# Exact Gate Review

Gate policy:
- Row must be selected by the source run.
- Source SQL must execute successfully.
- Candidate SQL must be generated.
- Candidate SQL must execute successfully.
- Local checker must report success.
- `exact_status` must be `exact`.

Gate result:

| case_id | selected | source executable | candidate generated | candidate executable | checker success | exact | eligible |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONS_0036 | true | true | true | true | true | true | true |
| CONS_0037 | true | true | true | true | true | true | true |

Both rows were eligible for VeriEQL execution. No ineligible row was silently dropped.

Result-checker exactness was used only as the entry gate. It was not used as verifier equivalence evidence.

