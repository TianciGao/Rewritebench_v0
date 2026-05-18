-- PERF_0011 minimal Spark SQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table lineitem
(
    l_partkey INT,
    l_extendedprice DECIMAL(15,2),
    l_discount DECIMAL(15,2),
    l_shipdate DATE
);

create table part
(
    p_partkey INT,
    p_type STRING
);
