-- case_id: PORT_0005
-- draft source id: PORT_PARROT_DRAFT_0006
-- draft-only / not validated
-- target dialect: mysql_like_positive
SELECT `nationality` FROM `drivers` WHERE NOT `dob` IS NULL ORDER BY `dob` IS NULL, `dob` ASC LIMIT 1
