-- PERF_0017 minimal Spark SQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table customer
(
    c_custkey INT,
    c_name STRING,
    c_address STRING,
    c_nationkey INT,
    c_phone STRING,
    c_acctbal DECIMAL(15,2),
    c_comment STRING
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
    l_extendedprice DECIMAL(15,2),
    l_discount DECIMAL(15,2),
    l_returnflag STRING
);

create table nation
(
    n_nationkey INT,
    n_name STRING
);
