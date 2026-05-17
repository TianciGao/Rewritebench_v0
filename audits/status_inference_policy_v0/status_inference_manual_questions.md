# status_inference_policy_v0 Manual Questions

- Does `ready=true` mean emitted candidate SQL plus extraction/readiness for each parser-v1 source family?
- Is `ready=true` sufficient evidence for a future Generation Rate numerator, or only for an audit-only dry-run support field?
- Does `exact=true` always imply that execution occurred in parser-v1 sources?
- Are `failure_stage` labels source-observed or parser-derived for P001, P002, P003, P011, and P012?
- Which failure-stage labels imply candidate SQL existed?
- Which failure-stage labels imply generation failed or no candidate exists?
- Which inferred fields may later be used in dry-run only?
- Which inferred fields, if any, may later be used in official metrics?
- Should inferred values be eligible only after a separate source-specific approval sheet?
- Should official metrics require observed fields only, with inferred fields limited to diagnostics?
