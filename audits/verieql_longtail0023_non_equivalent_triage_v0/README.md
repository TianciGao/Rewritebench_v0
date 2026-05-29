# verieql_longtail0023_non_equivalent_triage_v0

Task mode: local diagnostic triage only.

Branch: `feature/case-package-v2-external-schema`

Source run: `runs/user/common_core_pg_noop_db_checker`

Case: `LONGTAIL_0023`

Verdict: the `LONGTAIL_0023` `non_equivalent` result is not evidence of SQLGlot-noop candidate semantic drift. The source SQL and candidate SQL are byte-identical, and VeriEQL also returns `non_equivalent` for source-vs-source and candidate-vs-candidate at `bound_size=4`. The most likely classification is `possible_verieql_modeling_gap`, with `possible_bag_null_order_semantics_gap` as a secondary tool-semantics hypothesis.

Key findings:

- Exact gate reconfirmed: passed.
- Source/candidate SQL diff: no differences; byte-identical.
- Local retained result rows: source and candidate result JSONL files are identical for the retained witness.
- VeriEQL source-candidate recheck: `equivalent` at bound 1; `non_equivalent` at bounds 2, 3, and 4.
- VeriEQL source-source recheck at bound 4: `non_equivalent`.
- VeriEQL candidate-candidate recheck at bound 4: `non_equivalent`.

Paper boundary: `LONGTAIL_0023` must block any paper-facing Semantic Equivalence Rate promotion until the VeriEQL identity-pair failure is explained or excluded by an authorized policy.
