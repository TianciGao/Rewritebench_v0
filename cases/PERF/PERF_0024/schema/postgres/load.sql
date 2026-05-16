-- PERF_0024 minimal PostgreSQL witness data.
-- This is a deliberately tiny case-local dataset for first PostgreSQL validation only.
-- It is not a TPC-H scale dataset and does not imply MySQL/Spark readiness.

insert into nation (n_nationkey, n_name) values
    (1, 'BRAZIL'),
    (2, 'CANADA');

insert into supplier (s_suppkey, s_name, s_address, s_nationkey) values
    (10, 'Supplier#10', 'Brazil address', 1),
    (20, 'Supplier#20', 'Canada address', 2);

insert into part (p_partkey, p_name) values
    (100, 'pale green part'),
    (200, 'blue green part');

insert into partsupp (ps_partkey, ps_suppkey, ps_availqty) values
    (100, 10, 100),
    (200, 10, 10);

insert into lineitem (l_partkey, l_suppkey, l_quantity, l_shipdate) values
    (100, 10, 100.00, date '1997-06-01'),
    (200, 10, 100.00, date '1997-06-01');
