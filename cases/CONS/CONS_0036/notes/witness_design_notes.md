# Witness Design Notes

- Witness goal: prove `source = positive` and `source != negative` on a small case-local dataset.
- Expected positive mechanism: VeriEQL pair pushes a deterministic HAVING predicate below grouping.
- Expected hard-negative mechanism: Change the pushed predicate literal from Charlie to Alice.
- Witness complexity: small
