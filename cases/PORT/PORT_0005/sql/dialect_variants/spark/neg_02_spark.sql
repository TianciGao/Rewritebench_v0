-- case_id: PORT_0005
-- draft source id: PORT_PARROT_DRAFT_0006
-- draft-only / not validated
-- target dialect: spark_like_negative
-- DRAFT: Spark hard negative requires review
SELECT nationality
FROM drivers
WHERE dob IS NOT NULL
ORDER BY dob DESC
LIMIT 1
