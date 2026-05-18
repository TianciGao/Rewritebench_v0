-- PERF_0027 minimal MySQL witness data.
-- This is a deliberately tiny case-local dataset for MySQL validation only.
-- It is not a TPC-H scale dataset and does not imply Spark readiness.

insert into region (r_regionkey, r_name) values
    (1, 'MIDDLE EAST');

insert into nation (n_nationkey, n_name, n_regionkey) values
    (1, 'IRAN', 1),
    (2, 'IRAQ', 1),
    (3, 'JORDAN', 1);

insert into customer (c_custkey, c_nationkey) values
    (10, 3);

insert into orders (o_orderkey, o_custkey, o_orderdate) values
    (1000, 10, '1995-06-01'),
    (2000, 10, '1995-07-01'),
    (3000, 10, '1997-01-01');

insert into part (p_partkey, p_type) values
    (100, 'MEDIUM POLISHED STEEL'),
    (200, 'MEDIUM POLISHED STEEL');

insert into supplier (s_suppkey, s_nationkey) values
    (500, 1),
    (600, 2);

insert into lineitem (l_partkey, l_suppkey, l_orderkey, l_extendedprice, l_discount) values
    (100, 500, 1000, 100.00, 0.00),
    (200, 600, 2000, 50.00, 0.00),
    (100, 500, 3000, 999.00, 0.00);
