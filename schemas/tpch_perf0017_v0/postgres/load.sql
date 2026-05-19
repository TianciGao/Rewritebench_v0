-- PERF_0017 minimal PostgreSQL witness data.
-- This is a deliberately tiny case-local dataset for first PostgreSQL validation only.
-- It is not a TPC-H scale dataset and does not imply MySQL/Spark readiness.

insert into nation (n_nationkey, n_name) values
    (1, 'EGYPT'),
    (2, 'FRANCE');

insert into customer
    (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_comment)
values
    (1, 'Customer#1', 'Addr 1', 1, '10-001', 100.00, 'target customer'),
    (2, 'Customer#2', 'Addr 2', 2, '20-002', 200.00, 'negative-only customer');

insert into orders (o_orderkey, o_custkey, o_orderdate) values
    (100, 1, date '1993-12-01'),
    (101, 1, date '1994-03-01'),
    (200, 2, date '1993-12-15');

insert into lineitem (l_orderkey, l_extendedprice, l_discount, l_returnflag) values
    (100, 100.00, 0.10, 'R'),
    (101, 999.00, 0.00, 'R'),
    (200, 50.00, 0.00, 'A');
