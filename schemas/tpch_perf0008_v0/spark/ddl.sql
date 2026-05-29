-- PERF_0008 minimal Spark SQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table customer
(
    c_custkey INT,
    c_mktsegment STRING
);

create table orders
(
    o_orderkey INT,
    o_custkey INT,
    o_orderdate DATE,
    o_shippriority INT
);

create table lineitem
(
    l_orderkey INT,
    l_extendedprice DECIMAL(15,2),
    l_discount DECIMAL(15,2),
    l_shipdate DATE
);
