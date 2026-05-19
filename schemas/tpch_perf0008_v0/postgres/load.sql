-- PERF_0008 minimal PostgreSQL witness data.
-- This is a deliberately tiny case-local dataset for first PostgreSQL validation only.
-- It is not a TPC-H scale dataset and does not imply MySQL/Spark readiness.

insert into customer (c_custkey, c_mktsegment) values
    (1, 'MACHINERY'),
    (2, 'BUILDING'),
    (3, 'MACHINERY');

insert into orders (o_orderkey, o_custkey, o_orderdate, o_shippriority) values
    (100, 1, date '1995-03-01', 0),
    (200, 2, date '1995-03-01', 0),
    (300, 3, date '1995-04-01', 0);

insert into lineitem (l_orderkey, l_extendedprice, l_discount, l_shipdate) values
    (100, 100.00, 0.10, date '1995-04-01'),
    (200, 50.00, 0.00, date '1995-04-01'),
    (300, 999.00, 0.00, date '1995-04-02');
