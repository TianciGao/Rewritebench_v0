# Triage Verdict

Classification:

- Primary: `possible_verieql_modeling_gap`
- Secondary: `possible_bag_null_order_semantics_gap`
- Also retained: `unresolved_manual_review_required`

Rejected or not supported as primary classifications:

- `likely_candidate_semantic_drift`: not supported because source and candidate SQL are byte-identical.
- `possible_checker_false_accept`: not primary because the candidate did not differ from the source; the retained local witness also matched exactly.
- `possible_pair_construction_gap`: not supported because source-source and candidate-candidate identity support pairs also returned `non_equivalent`.
- `possible_schema_metadata_gap`: not primary because an identity query should remain equivalent regardless of missing constraints; however, schema/model handling may still be part of the VeriEQL tool-semantics gap.

Current conclusion:

- The `LONGTAIL_0023` `non_equivalent` row should be treated as a VeriEQL diagnostic artifact until proven otherwise.
- It must remain visible in local logs and excluded from paper-facing promotion.
- It should not be used to claim SQLGlot-noop semantic drift.
