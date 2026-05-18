-- PERF_0021 minimal MySQL witness data.
-- This is a deliberately tiny case-local dataset for MySQL validation only.
-- It is not a TPC-H scale dataset and does not imply Spark readiness.

insert into part (p_partkey, p_brand, p_container) values
    (1, 'Brand#31', 'JUMBO CASE'),
    (2, 'Brand#31', 'JUMBO BOX');

insert into lineitem (l_partkey, l_extendedprice, l_quantity) values
    (1, 70.00, 1.00),
    (1, 210.00, 20.00),
    (2, 700.00, 1.00),
    (2, 210.00, 20.00);
