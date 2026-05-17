# Candidate Status Overlap Policy Options

## Option A: Leave All 45 Overlap Rows Unauthorized

This is the safest short-term option. It avoids field-precedence ambiguity but leaves 45 filled parser-v1 rows unusable for metric-input authorization.

## Option B: Apply Source-Priority Rule For P001/P002/P003 Overlap

A future approved rule could treat P001 as generation/preflight readiness evidence, P002 as candidate-set status evidence, and P003 as Repair-1 failure enrichment only. This could resolve many rows, but it requires exact field-level precedence and validation that P003 never overrides successful P002 status.

## Option C: Require Manual Source-By-Source Selection

A maintainer reviews the 45 rows and explicitly selects the trusted source or field precedence for each overlap family before any authorization. This is slower than Option B but avoids silently codifying ambiguous status semantics.

## Option D: Rerun Parser With Normalized Source Precedence After Approval

A future parser version could materialize an approved normalized precedence policy and regenerate audit-only status output. This should happen only after Option B or C is approved, and it must remain non-timing and metrics-free unless separately authorized.

## Recommendation

Recommend Option C now. It keeps all 45 rows unauthorized until the maintainer approves field precedence. If a future automated policy is desired, approve Option D with explicit P001/P002/P003 precedence rules and a P003 failure-enrichment guard.
