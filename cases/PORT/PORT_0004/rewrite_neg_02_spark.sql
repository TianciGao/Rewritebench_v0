-- case_id: PORT_0004
-- draft source id: PORT_PARROT_DRAFT_0004
-- draft-only / not validated
-- target dialect: spark_like_negative
-- DRAFT: Spark hard negative requires review
SELECT CAST(SUM(CASE WHEN sex = 'F' THEN 1 ELSE 0 END) AS DOUBLE) * 100 / COUNT(id)
FROM patient
WHERE diagnosis = 'RA'
  AND YEAR(CAST(birthday AS DATE)) = 1981
