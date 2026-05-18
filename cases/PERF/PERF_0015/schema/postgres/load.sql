-- PERF_0015 minimal PostgreSQL witness data.
-- This is a deliberately tiny case-local dataset for first PostgreSQL validation only.
-- It is not a TPC-H scale dataset and does not imply MySQL/Spark readiness.

insert into region (r_regionkey, r_name) values
    (1, 'MIDDLE EAST');

insert into nation (n_nationkey, n_name, n_regionkey) values
    (10, 'IRAN', 1),
    (20, 'IRAQ', 1);

insert into supplier (s_suppkey, s_nationkey) values
    (100, 10),
    (200, 20);

insert into customer (c_custkey, c_nationkey) values
    (1, 10);

insert into orders (o_orderkey, o_custkey, o_orderdate) values
    (1000, 1, date '1995-06-01'),
    (2000, 1, date '1995-07-01'),
    (3000, 1, date '1997-01-01');

insert into part (p_partkey, p_type) values
    (1, 'MEDIUM POLISHED STEEL');

insert into lineitem
    (l_partkey, l_suppkey, l_orderkey, l_extendedprice, l_discount)
values
    (1, 100, 1000, 100.00, 0.00),
    (1, 200, 2000, 50.00, 0.00),
    (1, 100, 3000, 999.00, 0.00);
