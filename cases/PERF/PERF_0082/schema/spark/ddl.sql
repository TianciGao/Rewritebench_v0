-- Spark DDL for PERF_0082
-- draft_origin: JOB_DRAFT_0005

CREATE TABLE company_type (
  id INT,
  kind STRING
);

CREATE TABLE info_type (
  id INT
);

CREATE TABLE movie_companies (
  id INT,
  company_type_id INT,
  movie_id INT,
  note STRING
);

CREATE TABLE movie_info (
  id INT,
  info_type_id INT,
  info STRING,
  movie_id INT
);

CREATE TABLE title (
  id INT,
  production_year INT,
  title STRING
);
