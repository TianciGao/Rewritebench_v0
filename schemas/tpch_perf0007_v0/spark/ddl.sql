-- PERF_0007 minimal Spark SQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table lineitem
(
    l_shipdate DATE,
    l_discount DECIMAL(15,2),
    l_quantity DECIMAL(15,2),
    l_extendedprice DECIMAL(15,2)
);
