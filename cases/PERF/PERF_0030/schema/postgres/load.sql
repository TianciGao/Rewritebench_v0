-- PERF_0030 minimal PostgreSQL witness data.
-- Deliberately tiny case-local dataset for first PostgreSQL validation only.

insert into part (p_partkey, p_type) values
    (10, 'PROMO BRUSHED STEEL'),
    (20, 'STANDARD BRUSHED STEEL');

insert into lineitem (l_partkey, l_extendedprice, l_discount, l_shipdate) values
    (10, 100.00, 0.00, date '1997-03-10'),
    (20, 300.00, 0.00, date '1997-03-11'),
    (20, 500.00, 0.00, date '1997-04-10');
