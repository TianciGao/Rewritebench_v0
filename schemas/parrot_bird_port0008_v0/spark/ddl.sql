-- DRAFT DDL only; not executed in this task
CREATE TABLE frpm (cdscode STRING) USING parquet;
CREATE TABLE schools (cdscode STRING, county STRING, city STRING, doc STRING, opendate DATE, soc STRING, admemail1 STRING, admemail2 STRING) USING parquet;
