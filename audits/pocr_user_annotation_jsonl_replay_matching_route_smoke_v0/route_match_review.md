# Route Match Review

- Source annotation artifact: `audits/pocr_real_route_direct_llm_pg40_diagnostic_v0/safe_annotation_outputs.jsonl`
- Artifact route IDs: `{'direct_llm_original_pg40_pocr_diagnostic': 40}`
- Replay route ID used: `direct_llm_original_pg40_pocr_diagnostic`
- Route mismatch rows: `0`
- Artifact schema status counts: `{'fail': 7, 'pass': 33}`
- Replay annotation status counts: `{'schema_invalid': 7, 'schema_valid': 33}`
- Replay Stage B status counts: `{'schema_invalid': 7, 'transformation_evidence_partial': 23, 'presence_only': 6, 'insufficient_transformation_evidence': 4}`

The replay used the same route ID as the source annotation artifact, so strict route mapping did not reject rows. Existing malformed/schema-invalid artifact rows remained fail-closed as schema-invalid diagnostic rows.
