# Exact Gate Review

Gate policy:
- selected by source run
- source executable
- candidate generated
- candidate executable
- checker success
- exact/result-consistent under local result checker

Gate result:

| case_id | selected | source executable | candidate generated | candidate executable | checker success | exact | eligible |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONS_0036 | true | true | true | true | true | true | true |
| CONS_0037 | true | true | true | true | true | true | true |

Both rows were eligible and attempted. Local checker exactness was used only as an entry gate, not as verifier equivalence evidence.

