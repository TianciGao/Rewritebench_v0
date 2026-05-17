# Generation Rate Policy Questions For Team

The following questions remain unresolved for any future Generation Rate officialization task:

- Does `ready=true` mean emitted candidate SQL exists, or only that extraction/readiness checks passed after some upstream process?
- Can `inferred_generated=true` ever enter official Generation Rate input, or must official Generation Rate require source-observed `generated=true` only?
- If inference is allowed later, must observed generated and inferred generated be reported in separate columns and denominator partitions?
- Should Generation Rate remain a primary v0 metric if SQLGlot generated/ready evidence is missing?
- Should public v0 use a separate Generation/Readiness diagnostic table instead of official Generation Rate?
- What source-specific documentation is sufficient to prove ready-implies-generated semantics?
- Should official Generation Rate wait for additional observed generated evidence for SQLGlot routes?
- Can a future renderer show a blocked Generation Rate row in the appendix without rendering a main paper value?
- Should any future diagnostic support table be labeled audit-only, appendix-only, or public-support-only?
- What validation gate should prevent inferred-generated rows from being mistaken for observed generated evidence?
