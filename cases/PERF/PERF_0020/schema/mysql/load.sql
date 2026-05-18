-- PERF_0020 minimal MySQL witness data.
-- This is a deliberately tiny case-local dataset for MySQL validation only.
-- It is not a TPC-H scale dataset and does not imply Spark readiness.

insert into part (p_partkey, p_brand, p_type, p_size) values
    (1, 'Brand#10', 'SMALL BRUSHED', 42),
    (2, 'Brand#22', 'SMALL BRUSHED', 42),
    (3, 'Brand#23', 'SMALL BRUSHED', 42),
    (4, 'Brand#10', 'SMALL POLISHED STEEL', 42);

insert into supplier (s_suppkey, s_comment) values
    (100, 'reliable supplier'),
    (200, 'Customer Complaints recorded');

insert into partsupp (ps_partkey, ps_suppkey) values
    (1, 100),
    (1, 200),
    (2, 100),
    (3, 100),
    (4, 100);
