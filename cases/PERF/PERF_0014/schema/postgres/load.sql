-- PERF_0014 minimal PostgreSQL witness data.
-- This is a deliberately tiny case-local dataset for first PostgreSQL validation only.
-- It is not a TPC-H scale dataset and does not imply MySQL/Spark readiness.

insert into nation (n_nationkey, n_name) values
    (1, 'BRAZIL'),
    (2, 'MOROCCO');

insert into supplier (s_suppkey, s_nationkey) values
    (100, 1),
    (200, 2);

insert into customer (c_custkey, c_nationkey) values
    (10, 2),
    (20, 1);

insert into orders (o_orderkey, o_custkey) values
    (1000, 10),
    (2000, 20);

insert into lineitem
    (l_orderkey, l_suppkey, l_shipdate, l_extendedprice, l_discount)
values
    (1000, 100, date '1995-06-01', 100.00, 0.10),
    (2000, 200, date '1996-06-01', 50.00, 0.00);
