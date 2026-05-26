
# Retry Quality Comparison

Before retry:

- schema-valid rows = 35
- fail-closed rows = 5
- transformation-supported operation atoms = 32
- presence-only atoms = 10
- insufficient-transformation-evidence atoms = 50

After retry:

- schema-valid rows = 40
- remaining fail-closed rows = 0
- transformation-supported operation atoms = 41
- presence-only atoms = 11
- insufficient-transformation-evidence atoms = 55

The targeted retry improved artifact completeness by replacing all five fail-closed annotation rows with schema-valid retry rows. The resulting counts are diagnostic counts only. This task does not claim official POCR and does not authorize paper-facing metric promotion.
