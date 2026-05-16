-- PERF_0019 minimal MySQL witness data.
-- This is a deliberately tiny case-local dataset for MySQL validation only.
-- It is not a TPC-H scale dataset and does not imply Spark readiness.

insert into customer (c_custkey) values
    (1),
    (2),
    (3);

insert into orders (o_orderkey, o_custkey, o_comment) values
    (100, 1, 'ordinary order'),
    (101, 1, 'express handling deposits included'),
    (200, 2, 'special handling deposits included');
