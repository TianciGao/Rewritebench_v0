-- case_id: PORT_0006
-- draft source id: PORT_PARROT_DRAFT_0011
-- draft-only / not validated
-- source dialect: mysql_like_candidate
SELECT CAST( SUM( `status` = 'C' ) AS DOUBLE ) * 100 / COUNT( `account_id` ) FROM `loan` WHERE `amount` < 100000
