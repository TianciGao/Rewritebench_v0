-- PERF_0031 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It is not a TPC-H scale dataset and does not imply PostgreSQL/MySQL readiness.

insert into supplier (s_suppkey, s_name, s_address, s_phone) values
    (100, 'Supplier#000000100', 'Address 100', '10-100-100-1000'),
    (200, 'Supplier#000000200', 'Address 200', '20-200-200-2000');

insert into lineitem (l_suppkey, l_extendedprice, l_discount, l_shipdate) values
    (100, 100.00, 0.00, date '1994-06-15'),
    (200, 50.00, 0.00, date '1994-07-15'),
    (200, 999.00, 0.00, date '1994-10-01');
