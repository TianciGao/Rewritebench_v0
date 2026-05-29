# POCR No-API Parser Adapter v0

This packet records the implementation scaffold and parse-only validation for the Common-core root-level `skills.md` POCR contract.

Implemented modules:

- `src/sql_rewrite_bench/pocr/__init__.py`
- `src/sql_rewrite_bench/pocr/models.py`
- `src/sql_rewrite_bench/pocr/skills_parser.py`
- `src/sql_rewrite_bench/pocr/validation.py`
- `src/sql_rewrite_bench/pocr/inventory.py`

Tests:

- `tests/pocr/test_skills_parser.py`
- `tests/pocr/test_skills_inventory.py`

Parse-only inventory result:

- Common-core skills parsed: 40
- Valid contracts: 40
- Pool split: PERF 16, CONS 9, PORT 9, LONGTAIL 6
- Total parsed atoms: 187
- Parsed `operation_atom` rows: 107
- Parsed `semantic_guard_atom` rows: 80
- Validation issues: 0

Audit-only CSV outputs:

- `parsed_skills_inventory.csv`
- `atom_inventory.csv`
- `validation_issues.csv`

Boundaries:

- No live API call.
- No DB/checker/timing run.
- No baseline rerun.
- No official Positive Operation Coverage Rate computation.
- No candidate SQL judgment.
- No Stage A annotation.
- No Stage B evidence validation.
- No case package file modification.
- No `skill/` directory creation.
- No `output/`, top-level `reports/`, top-level `results/`, or case-local `runs/` output.

Next safe action: design API annotation plus Stage B evidence-validation interfaces, still without full-route POCR computation.
