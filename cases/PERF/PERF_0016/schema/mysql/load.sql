-- PERF_0016 minimal PostgreSQL witness data.
-- This is a deliberately tiny case-local dataset for first PostgreSQL validation only.
-- It is not a TPC-H scale dataset and does not imply MySQL/Spark readiness.

insert into nation (n_nationkey, n_name) values
    (1, 'BRAZIL'),
    (2, 'EGYPT');

insert into supplier (s_suppkey, s_nationkey) values
    (100, 1),
    (200, 2);

insert into orders (o_orderkey, o_orderdate) values
    (1000, date '1995-01-01'),
    (2000, date '1996-01-01');

insert into part (p_partkey, p_name) values
    (1, 'turquoise widget'),
    (2, 'green widget');

insert into lineitem
    (l_partkey, l_suppkey, l_orderkey, l_extendedprice, l_discount, l_quantity)
values
    (1, 100, 1000, 100.00, 0.00, 2.00),
    (2, 200, 2000, 50.00, 0.00, 1.00);

insert into partsupp (ps_partkey, ps_suppkey, ps_supplycost) values
    (1, 100, 10.00),
    (2, 200, 5.00);
