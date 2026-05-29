-- MySQL witness data for PERF_0082
-- draft_origin: JOB_DRAFT_0005

INSERT INTO company_type (id, kind) VALUES (1, 'production companies');
INSERT INTO company_type (id, kind) VALUES (2, 'distributors');

INSERT INTO info_type (id) VALUES (1);

INSERT INTO movie_companies (id, company_type_id, movie_id, note) VALUES (1, 1, 1, '(theatrical) (France)');
INSERT INTO movie_companies (id, company_type_id, movie_id, note) VALUES (2, 2, 2, '(theatrical) (France)');
INSERT INTO movie_companies (id, company_type_id, movie_id, note) VALUES (3, 1, 3, '(television) (France)');

INSERT INTO movie_info (id, info_type_id, info, movie_id) VALUES (1, 1, 'Sweden', 1);
INSERT INTO movie_info (id, info_type_id, info, movie_id) VALUES (2, 1, 'Germany', 2);
INSERT INTO movie_info (id, info_type_id, info, movie_id) VALUES (3, 1, 'Spain', 3);

INSERT INTO title (id, production_year, title) VALUES (1, 2006, 'Alpha European');
INSERT INTO title (id, production_year, title) VALUES (2, 2007, 'Beta European');
INSERT INTO title (id, production_year, title) VALUES (3, 2008, 'Gamma Guardrail');
