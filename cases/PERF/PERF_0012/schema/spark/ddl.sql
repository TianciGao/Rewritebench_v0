-- PERF_0012 minimal Spark SQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table part
(
    p_partkey INT,
    p_mfgr STRING,
    p_size INT,
    p_type STRING
);

create table supplier
(
    s_suppkey INT,
    s_name STRING,
    s_address STRING,
    s_nationkey INT,
    s_phone STRING,
    s_acctbal DECIMAL(15,2),
    s_comment STRING
);

create table partsupp
(
    ps_partkey INT,
    ps_suppkey INT,
    ps_supplycost DECIMAL(15,2)
);

create table nation
(
    n_nationkey INT,
    n_name STRING,
    n_regionkey INT
);

create table region
(
    r_regionkey INT,
    r_name STRING
);
