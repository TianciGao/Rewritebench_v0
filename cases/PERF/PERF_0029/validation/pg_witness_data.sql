-- PERF_0029 minimal PostgreSQL witness data.
-- Deliberately tiny case-local dataset for first PostgreSQL validation only.

insert into customer (c_custkey) values
    (1),
    (2),
    (3);

insert into orders (o_orderkey, o_custkey, o_comment) values
    (10, 1, 'ordinary shipment'),
    (11, 1, 'express deposits delayed'),
    (20, 2, 'ordinary request');
