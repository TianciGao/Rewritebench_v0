# CONS_0011 Migration Notes

Migration date: 2026-05-16.

This package was migrated with a copy-first canonical layout principle. Public-safe files were copied from the legacy case package; generated metadata summarizes retained legacy facts only. Legacy repo unchanged: yes. Raw legacy evidence unchanged: yes.

Maintainer-approved hard-negative reason: rewrite_neg_01 changes a NULL-preserving LEFT JOIN / IS NULL existence test into an INNER JOIN match test. This breaks outer-join NULL preservation. Therefore neg_01 is an intentional hard negative and should be rejected by the checker. Expected rejection reason: `outer_join_null_preservation_changed`. Approval status: maintainer_approved_for_migration.

Spark plan sanitization: sanitized Spark plan copies were generated under `evidence/retained_plans/spark/`; raw Spark plan text remains mapped as do-not-delete legacy evidence and was not copied raw.

Validation script output-policy caveat: copied/adapted scripts are retained legacy validation assets, were not executed during migration, and future public runners should write outputs outside case-local runs by default.

Denominator unchanged: yes. Paper results unchanged: yes. Common-core membership unchanged: yes.
