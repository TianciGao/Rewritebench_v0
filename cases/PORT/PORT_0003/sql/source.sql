-- case_id: PORT_0003
-- draft source id: PORT_PARROT_DRAFT_0002
-- draft-only / not validated
-- source dialect: postgres_like_candidate
SELECT "gsoffered" FROM "schools" ORDER BY ABS( "longitude" ) DESC NULLS LAST LIMIT 1
