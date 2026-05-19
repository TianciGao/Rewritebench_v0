-- case_id: PORT_0003
-- draft source id: PORT_PARROT_DRAFT_0002
-- draft-only / not validated
-- target dialect: mysql_like_negative
SELECT `gsoffered` FROM `schools` ORDER BY ABS(`longitude`) ASC LIMIT 1
