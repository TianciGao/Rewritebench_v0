-- PERF_0018 minimal Spark SQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table partsupp
(
    ps_partkey INT,
    ps_suppkey INT,
    ps_supplycost DECIMAL(15,2),
    ps_availqty INT
);

create table supplier
(
    s_suppkey INT,
    s_nationkey INT
);

create table nation
(
    n_nationkey INT,
    n_name STRING
);
