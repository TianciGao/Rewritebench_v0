-- Case-local MySQL witness data for PERF_0077
-- Not executed in this task.

INSERT INTO keyword (id, keyword) VALUES (1, 'presequelpost');
INSERT INTO keyword (id, keyword) VALUES (2, 'sequel-start');
INSERT INTO keyword (id, keyword) VALUES (3, 'standalone');

INSERT INTO movie_info (id, info, movie_id) VALUES (1, 'Sweden', 1);
INSERT INTO movie_info (id, info, movie_id) VALUES (2, 'Germany', 2);
INSERT INTO movie_info (id, info, movie_id) VALUES (3, 'Norway', 3);

INSERT INTO movie_keyword (id, keyword_id, movie_id) VALUES (1, 1, 1);
INSERT INTO movie_keyword (id, keyword_id, movie_id) VALUES (2, 2, 2);
INSERT INTO movie_keyword (id, keyword_id, movie_id) VALUES (3, 3, 3);

INSERT INTO title (id, production_year, title) VALUES (1, 2006, 'Alpha Movie');
INSERT INTO title (id, production_year, title) VALUES (2, 2007, 'Beta Movie');
INSERT INTO title (id, production_year, title) VALUES (3, 2008, 'Gamma Movie');
