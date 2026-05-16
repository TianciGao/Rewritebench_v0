# Witness Design Notes

- Witness goal: prove `source = positive` and `source != negative` on a small case-local dataset.
- Expected positive mechanism: VeriEQL pair preserves COUNT(DISTINCT joined attribute) while simplifying aliasing and grouping.
- Expected hard-negative mechanism: Drop DISTINCT from the joined-name count.
- Witness complexity: small
