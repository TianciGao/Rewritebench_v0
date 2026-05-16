# PERF_0006 Risk Notes

- Performance-sensitive packaging can be misread as a new speedup claim. Mitigation: manifest, README, metadata, and evidence summaries all record `speedup_claim_created: false`.
- Retained validation assets still reflect legacy output conventions. Mitigation: scripts are documented as legacy validation assets and future public runner output must not write to case-local runs/ by default.
- Spark plan text contained local temporary path traces. Mitigation: raw Spark plan text is mapped as do-not-delete legacy evidence, and sanitized derivatives are published under `evidence/retained_plans/spark/`.
- This pilot does not change Common-core membership, denominator, or paper results.
