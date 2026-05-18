-- PERF_0016 minimal Spark SQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table part
(
    p_partkey INT,
    p_name STRING
);

create table supplier
(
    s_suppkey INT,
    s_nationkey INT
);

create table lineitem
(
    l_partkey INT,
    l_suppkey INT,
    l_orderkey INT,
    l_extendedprice DECIMAL(15,2),
    l_discount DECIMAL(15,2),
    l_quantity DECIMAL(15,2)
);

create table partsupp
(
    ps_partkey INT,
    ps_suppkey INT,
    ps_supplycost DECIMAL(15,2)
);

create table orders
(
    o_orderkey INT,
    o_orderdate DATE
);

create table nation
(
    n_nationkey INT,
    n_name STRING
);
