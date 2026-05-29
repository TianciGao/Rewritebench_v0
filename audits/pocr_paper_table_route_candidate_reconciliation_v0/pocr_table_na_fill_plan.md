# POCR Table N.A. Fill Plan

No Positive Operation Coverage Rate value can be filled now. This task computes no official POCR, emits no route-level POCR score, and promotes no paper-facing metric.

| Table row | Classification | Can fill now? | Missing prerequisite | Future scope |
| --- | --- | --- | --- | --- |
| Direct LLM original | diagnostic_TrackA120_possible_after_annotation | no | Tri-engine route-bound annotation JSONL and separate diagnostic/promotion authorization | Diagnostic Track A 120 possible after annotation |
| Direct LLM + Repair-1 | diagnostic_TrackA120_possible_after_annotation | no | Route-bound annotation JSONL and separate diagnostic/promotion authorization | PG40 first, then diagnostic Track A 120 if authorized |
| SQLGlot no-op | diagnostic_PG40_possible | no | Track A 120 candidate family incomplete; PG40 annotation not generated | PG40 sanity/control diagnostic only |
| SQLGlot optimize schema-aware | candidate_root_missing_or_ambiguous | no | Complete candidate roots or explicit no-candidate policy | Deferred |
| Calcite HEP fail-closed | candidate_root_missing_or_ambiguous | no | Complete candidate roots or explicit fail-closed/no-candidate policy | Deferred |
| LearnedRewrite | candidate_root_missing_or_ambiguous | no | PG40 full-denominator candidate handling; only 29 generated candidates present | Deferred or generated-row diagnostic only |
| R-Bot adapted GPT-5.4 | diagnostic_PG40_possible | no | Route-bound annotation JSONL and replay task | Diagnostic PG40 only |
| LLM-R2 adapted GPT-5.4 | diagnostic_PG40_possible | no | Route-bound annotation JSONL and replay task | Diagnostic PG40 only |

Any future fill remains diagnostic-only unless a separate official POCR and paper metric promotion task is authorized.
