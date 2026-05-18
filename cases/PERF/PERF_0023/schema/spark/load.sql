-- PERF_0023 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It is not a TPC-H scale dataset and does not imply PostgreSQL/MySQL readiness.

insert into part (p_partkey, p_brand, p_container, p_size) values
    (1, 'Brand#14', 'SM CASE', 3);

insert into lineitem
    (l_partkey, l_extendedprice, l_discount, l_quantity, l_shipmode, l_shipinstruct)
values
    (1, 100.00, 0.10, 5.00, 'AIR', 'DELIVER IN PERSON');
