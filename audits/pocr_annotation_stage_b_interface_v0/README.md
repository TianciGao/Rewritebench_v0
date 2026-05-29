# POCR Annotation And Stage B Interface v0

This packet records the offline scaffold for the next POCR layer after the D036 `skills.md` parser.

Implemented source files:

- `src/sql_rewrite_bench/pocr/annotation_schema.py`
- `src/sql_rewrite_bench/pocr/prompt_builder.py`
- `src/sql_rewrite_bench/pocr/annotation_client.py`
- `src/sql_rewrite_bench/pocr/evidence_validation.py`
- `src/sql_rewrite_bench/pocr/pocr_row.py`
- `src/sql_rewrite_bench/pocr/__init__.py`

Implemented tests:

- `tests/pocr/test_annotation_schema.py`
- `tests/pocr/test_prompt_builder.py`
- `tests/pocr/test_evidence_validation.py`

Fixture coverage:

- `PERF_0006`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

The packet includes fixture-only Stage A annotation examples and Stage B validation examples. Stage B is fail-closed: without independent evidence, atoms remain `insufficient_evidence`; LLM rationale, speedup, timing, and taxonomy tags are not evidence for atom implementation.

Boundaries:

- No live API call.
- No API key read.
- No DB/checker/timing run.
- No baseline rerun.
- No official Positive Operation Coverage Rate computation.
- No route-level POCR aggregation.
- No case package or `skills.md` modification.
- No `skill/` directory creation.
- No `output/`, top-level `reports/`, top-level `results/`, or case-local `runs/` output.

Next safe action: review this interface packet, then authorize a 2-4 case offline-to-live API annotation smoke only if the fail-closed Stage B boundary is accepted.
