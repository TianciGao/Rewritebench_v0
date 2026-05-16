-- case_id: PORT_0003
-- draft source id: PORT_PARROT_DRAFT_0002
-- draft-only / not validated
-- target dialect: spark_like_positive
-- DRAFT: Spark adaptation requires review
SELECT gsoffered
FROM schools
ORDER BY CASE WHEN longitude IS NULL THEN 1 ELSE 0 END, ABS(longitude) DESC
LIMIT 1
