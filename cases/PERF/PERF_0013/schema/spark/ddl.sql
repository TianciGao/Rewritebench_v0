-- PERF_0013 minimal Spark SQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table customer
(
    c_custkey INT,
    c_nationkey INT
);

create table orders
(
    o_orderkey INT,
    o_custkey INT,
    o_orderdate DATE
);

create table lineitem
(
    l_orderkey INT,
    l_suppkey INT,
    l_extendedprice DECIMAL(15,2),
    l_discount DECIMAL(15,2)
);

create table supplier
(
    s_suppkey INT,
    s_nationkey INT
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
