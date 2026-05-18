-- PERF_0009 minimal Spark SQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table orders
(
    o_orderkey INT,
    o_orderpriority STRING,
    o_orderdate DATE
);

create table lineitem
(
    l_orderkey INT,
    l_commitdate DATE,
    l_receiptdate DATE
);
