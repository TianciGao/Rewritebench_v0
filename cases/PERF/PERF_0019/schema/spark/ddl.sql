-- PERF_0019 minimal Spark SQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table customer
(
    c_custkey INT
);

create table orders
(
    o_orderkey INT,
    o_custkey INT,
    o_comment STRING
);
