-- PERF_0010 minimal PostgreSQL witness data.
-- This is a deliberately tiny case-local dataset for first PostgreSQL validation only.
-- It is not a TPC-H scale dataset and does not imply MySQL/Spark readiness.

insert into orders (o_orderkey, o_orderpriority) values
    (500, '1-URGENT'),
    (501, '3-MEDIUM'),
    (502, '2-HIGH');

insert into lineitem (l_orderkey, l_shipmode, l_commitdate, l_receiptdate, l_shipdate) values
    (500, 'REG AIR', date '1993-01-10', date '1993-01-12', date '1993-01-08'),
    (501, 'RAIL', date '1993-02-10', date '1993-02-12', date '1993-02-08'),
    (502, 'SHIP', date '1993-03-10', date '1993-03-12', date '1993-03-08');
