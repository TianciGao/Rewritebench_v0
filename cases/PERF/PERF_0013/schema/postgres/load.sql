-- PERF_0013 minimal PostgreSQL witness data.
-- This is a deliberately tiny case-local dataset for first PostgreSQL validation only.
-- It is not a TPC-H scale dataset and does not imply MySQL/Spark readiness.

insert into region (r_regionkey, r_name) values
    (1, 'MIDDLE EAST'),
    (2, 'EUROPE');

insert into nation (n_nationkey, n_name, n_regionkey) values
    (10, 'EGYPT', 1),
    (20, 'GERMANY', 2);

insert into supplier (s_suppkey, s_nationkey) values
    (100, 10),
    (200, 20);

insert into customer (c_custkey, c_nationkey) values
    (1, 10),
    (2, 20);

insert into orders (o_orderkey, o_custkey, o_orderdate) values
    (500, 1, date '1997-06-01'),
    (600, 2, date '1997-06-01'),
    (700, 1, date '1998-02-01');

insert into lineitem (l_orderkey, l_suppkey, l_extendedprice, l_discount) values
    (500, 100, 100.00, 0.10),
    (600, 200, 50.00, 0.00),
    (700, 100, 999.00, 0.00);
