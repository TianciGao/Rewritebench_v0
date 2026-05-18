-- PERF_0028 minimal PostgreSQL witness data.
-- Deliberately tiny case-local dataset for first PostgreSQL validation only.

insert into orders (o_orderkey, o_orderpriority) values
    (500, '1-URGENT'),
    (501, '3-MEDIUM'),
    (502, '2-HIGH');

insert into lineitem (l_orderkey, l_shipmode, l_commitdate, l_receiptdate, l_shipdate) values
    (500, 'REG AIR', date '1993-01-10', date '1993-01-12', date '1993-01-08'),
    (501, 'RAIL', date '1993-02-10', date '1993-02-12', date '1993-02-08'),
    (502, 'REG AIR', date '1993-03-10', date '1993-03-12', date '1993-03-08');
