-- case_id: PORT_0004
-- draft source id: PORT_PARROT_DRAFT_0004
-- draft-only / not validated
-- source dialect: mysql_like_candidate
SELECT CAST( SUM( CASE WHEN `sex` = 'F' THEN 1 ELSE 0 END ) AS DOUBLE ) * 100 / COUNT( `id` ) FROM `patient` WHERE `diagnosis` = 'RA' AND DATE_FORMAT( CAST( `birthday` AS DATETIME ) , '%Y' ) = '1980'
