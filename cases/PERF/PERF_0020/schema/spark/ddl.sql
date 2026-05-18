-- PERF_0020 minimal Spark SQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table partsupp
(
    ps_partkey INT,
    ps_suppkey INT
);

create table part
(
    p_partkey INT,
    p_brand STRING,
    p_type STRING,
    p_size INT
);

create table supplier
(
    s_suppkey INT,
    s_comment STRING
);
