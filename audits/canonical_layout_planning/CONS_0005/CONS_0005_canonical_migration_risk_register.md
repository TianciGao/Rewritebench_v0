# CONS_0005 Canonical Migration Risk Register

## R1: Checker Semantics Not Fully Inferable From Static Files

- Severity: high
- Affected files: `rewrite_neg_01.sql`, `validation/check_results.py`, retained TSV outputs, future `checker/*.yaml`
- Mitigation: human review must approve the expected rejection reason before actual migration marks the case canonical-complete.
- Blocks actual migration: yes, if no approval is available.

## R2: Hard-Negative Expected Reason Missing Or Unclear

- Severity: high
- Affected files: `checker/expected_rejections.yaml`, `evidence/hard_negative/`
- Mitigation: encode `null_semantics_not_preserved_for_correlated_not_in` only after review; otherwise mark `needs_human_review`.
- Blocks actual migration: yes.

## R3: Validation Scripts Write To Case-Local runs/

- Severity: medium
- Affected files: `validation/run_*_validation.sh`, `validation/run_*_plan_collection.sh`
- Mitigation: copied scripts must be labeled legacy validation assets or wrapped so future public runner output does not write to case-local `runs/` by default.
- Blocks actual migration: yes, if no output-policy caveat exists.

## R4: Raw runs/ Retention Ambiguity

- Severity: medium
- Affected files: `runs/`
- Mitigation: create complete `evidence/runs_retention.yaml`; do not copy raw `runs/` wholesale; promote only reviewed public-safe evidence.
- Blocks actual migration: yes.

## R5: Spark Plan Local Temporary Paths

- Severity: high
- Affected files: `runs/spark/plans/source.txt`, `runs/spark/plans/rewrite_pos_01.txt`, `runs/spark/plans/rewrite_neg_01.txt`
- Mitigation: create sanitized public copies or keep raw files private/archive-only; map original files as do-not-delete.
- Blocks actual migration: yes, if raw paths remain in public files.

## R6: Spark Validation WSL Wording

- Severity: medium
- Affected files: `validation/run_spark_validation.sh`, `validation/run_spark_plan_collection.sh`
- Mitigation: remove WSL-local wording or mark scripts as legacy assets with clear execution caveat.
- Blocks actual migration: yes, if canonical hygiene scan fails.

## R7: Overclaiming Denominator Or Paper Results

- Severity: high
- Affected files: `manifest.yaml`, `metadata/denominator_eligibility.yaml`, `README.md`, `notes/migration_notes.md`
- Mitigation: keep denominator, paper results, Common-core membership, admission, DB validation, and evidence regeneration flags false.
- Blocks actual migration: yes.

## R8: Generated Taxonomy Overreach

- Severity: medium
- Affected files: `metadata/taxonomy.yaml`
- Mitigation: preserve legacy manifest tags conservatively and record that formal taxonomy review remains separate.
- Blocks actual migration: no, if clearly caveated; yes, if it implies admission or promotion.
