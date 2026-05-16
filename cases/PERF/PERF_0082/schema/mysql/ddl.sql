-- MySQL DDL for PERF_0082
-- draft_origin: JOB_DRAFT_0005

CREATE TABLE company_type (
  id INT,
  kind TEXT
);

CREATE TABLE info_type (
  id INT
);

CREATE TABLE movie_companies (
  id INT,
  company_type_id INT,
  movie_id INT,
  note TEXT
);

CREATE TABLE movie_info (
  id INT,
  info_type_id INT,
  info TEXT,
  movie_id INT
);

CREATE TABLE title (
  id INT,
  production_year INT,
  title TEXT
);
