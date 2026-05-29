-- Minimal MySQL DDL for PERF_0077
-- Case-local construction only; not yet validated as an official case.

CREATE TABLE keyword (
  id INT,
  keyword TEXT
);

CREATE TABLE movie_info (
  id INT,
  info TEXT,
  movie_id INT
);

CREATE TABLE movie_keyword (
  id INT,
  keyword_id INT,
  movie_id INT
);

CREATE TABLE title (
  id INT,
  production_year INT,
  title TEXT
);
