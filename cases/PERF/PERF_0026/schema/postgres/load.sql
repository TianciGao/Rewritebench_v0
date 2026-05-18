-- PERF_0026 minimal PostgreSQL witness data.
-- This is a deliberately tiny case-local dataset for first PostgreSQL validation only.
-- It is not a TPC-H scale dataset and does not imply MySQL/Spark readiness.

insert into customer (c_custkey, c_phone, c_acctbal) values
    (1, '19-111-1111', 100.00),
    (2, '29-222-2222', 10.00),
    (3, '18-333-3333', 1000.00);

insert into orders (o_custkey) values
    (3);
