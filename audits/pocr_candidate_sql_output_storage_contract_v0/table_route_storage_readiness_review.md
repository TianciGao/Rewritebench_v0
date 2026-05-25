# Table Route Storage Readiness Review

This review uses the Step 1b route reconciliation packet as source context.

| Table route | PG40 readiness | Track A 120 readiness | Storage interpretation |
| --- | --- | --- | --- |
| Direct LLM original | yes | yes | Complete PostgreSQL PG40 root and complete tri-engine family exist. POCR remains N.A. pending annotation JSONL and promotion policy. |
| Direct LLM Repair-1 | yes | yes | Complete PostgreSQL PG40 root and complete tri-engine family exist. Recommended next diagnostic route is PostgreSQL PG40. |
| SQLGlot no-op | yes | no | Complete PG40 no-op root exists, but canonical Track A roots are incomplete. PG40 only. |
| SQLGlot optimize schema-aware | no | no | Existing candidate roots are incomplete. Requires no-candidate/fail-closed policy before POCR annotation. |
| Calcite HEP fail-closed | no | no | Existing candidate roots are incomplete by fail-closed behavior. Requires no-candidate/fail-closed policy before POCR annotation. |
| LearnedRewrite | no | not applicable | Only 29 generated PostgreSQL candidate files are present for PG40. |
| R-Bot adapted GPT-5.4 | yes | not applicable | Complete PG40 prior-method root exists. Diagnostic PG40 annotation could be separately authorized. |
| LLM-R2 adapted GPT-5.4 | yes | not applicable | Complete PG40 prior-method root exists. Diagnostic PG40 annotation could be separately authorized. |

The Positive Operation Coverage Rate column remains deferred / N.A. for every row now. Candidate SQL readiness is not annotation readiness and is not official POCR.

PG40 candidate roots cannot fill Track A 120 POCR cells. No official POCR is computed. No paper-facing metric is promoted. No route-level POCR score is emitted.
