-- PERF_0021 minimal Spark SQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table lineitem
(
    l_partkey INT,
    l_extendedprice DECIMAL(15,2),
    l_quantity DECIMAL(15,2)
);

create table part
(
    p_partkey INT,
    p_brand STRING,
    p_container STRING
);
