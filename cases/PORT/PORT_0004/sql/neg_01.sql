-- case_id: PORT_0004
-- draft source id: PORT_PARROT_DRAFT_0004
-- draft-only / not validated
-- target dialect: postgres_like_negative
SELECT CAST( SUM( CASE WHEN "sex" = 'F' THEN 1 ELSE 0 END ) AS DOUBLE PRECISION ) * 100 / COUNT( "id" ) FROM "patient" WHERE "diagnosis" = 'RA' AND EXTRACT(YEAR FROM CAST( "birthday" AS TIMESTAMP )) = '1981'
