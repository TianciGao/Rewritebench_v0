-- PERF_0009 minimal PostgreSQL witness data.
-- This is a deliberately tiny case-local dataset for first PostgreSQL validation only.
-- It is not a TPC-H scale dataset and does not imply MySQL/Spark readiness.

insert into orders (o_orderkey, o_orderpriority, o_orderdate) values
    (400, '1-URGENT', date '1996-11-15'),
    (401, '2-HIGH', date '1996-11-20'),
    (402, '3-MEDIUM', date '1997-03-01');

insert into lineitem (l_orderkey, l_commitdate, l_receiptdate) values
    (400, date '1996-11-16', date '1996-11-18'),
    (401, date '1996-11-20', date '1996-11-20'),
    (402, date '1997-03-02', date '1997-03-03');
