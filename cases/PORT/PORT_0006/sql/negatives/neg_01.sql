-- case_id: PORT_0006
-- draft source id: PORT_PARROT_DRAFT_0011
-- draft-only / not validated
-- target dialect: postgres_like_negative
SELECT CAST( COUNT( CASE WHEN "status" = 'C' THEN 1 END ) AS DOUBLE PRECISION ) * 100 / COUNT( "account_id" ) FROM "loan" WHERE "amount" <= 100000
