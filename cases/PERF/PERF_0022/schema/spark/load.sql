-- PERF_0022 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It is not a TPC-H scale dataset and does not imply PostgreSQL/MySQL readiness.

insert into customer (c_custkey, c_name) values
    (1, 'Customer#1'),
    (2, 'Customer#2');

insert into orders (o_orderkey, o_custkey, o_orderdate, o_totalprice) values
    (100, 1, date '1995-01-01', 1000.00),
    (200, 2, date '1995-01-02', 500.00);

insert into lineitem (l_orderkey, l_quantity) values
    (100, 160.00),
    (100, 160.00),
    (200, 150.00),
    (200, 155.00);
