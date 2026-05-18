-- PERF_0018 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It is not a TPC-H scale dataset and does not imply PostgreSQL/MySQL readiness.

insert into nation (n_nationkey, n_name) values
    (1, 'EGYPT'),
    (2, 'FRANCE');

insert into supplier (s_suppkey, s_nationkey) values
    (100, 1),
    (101, 1),
    (200, 2);

insert into partsupp (ps_partkey, ps_suppkey, ps_supplycost, ps_availqty) values
    (10, 100, 100.00, 10),
    (20, 101, 10.00, 10),
    (30, 200, 50.00, 1);
