-- PERF_0010 minimal Spark SQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table orders
(
    o_orderkey INT,
    o_orderpriority STRING
);

create table lineitem
(
    l_orderkey INT,
    l_shipmode STRING,
    l_commitdate DATE,
    l_receiptdate DATE,
    l_shipdate DATE
);
