-- PERF_0025 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It is not a TPC-H scale dataset and does not imply PostgreSQL/MySQL readiness.

insert into nation (n_nationkey, n_name) values
    (1, 'IRAQ'),
    (2, 'IRAN');

insert into supplier (s_suppkey, s_name, s_nationkey) values
    (10, 'Supplier#10', 1),
    (20, 'Supplier#20', 1),
    (30, 'Supplier#30', 2);

insert into orders (o_orderkey, o_orderstatus) values
    (100, 'F');

insert into lineitem (l_orderkey, l_suppkey, l_receiptdate, l_commitdate) values
    (100, 10, date '1995-01-10', date '1995-01-05'),
    (100, 20, date '1995-01-04', date '1995-01-05');
