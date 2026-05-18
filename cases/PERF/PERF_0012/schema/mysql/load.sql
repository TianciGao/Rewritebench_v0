-- PERF_0012 minimal PostgreSQL witness data.
-- This is a deliberately tiny case-local dataset for first PostgreSQL validation only.
-- It is not a TPC-H scale dataset and does not imply MySQL/Spark readiness.

insert into region (r_regionkey, r_name) values
    (1, 'MIDDLE EAST'),
    (2, 'EUROPE');

insert into nation (n_nationkey, n_name, n_regionkey) values
    (10, 'EGYPT', 1),
    (20, 'FRANCE', 2);

insert into supplier
    (s_suppkey, s_name, s_address, s_nationkey, s_phone, s_acctbal, s_comment)
values
    (100, 'Supplier#100', 'Addr 100', 10, '10-100', 1000.00, 'target supplier'),
    (101, 'Supplier#101', 'Addr 101', 10, '10-101', 500.00, 'alternate supplier'),
    (200, 'Supplier#200', 'Addr 200', 20, '20-200', 900.00, 'non-target region');

insert into part (p_partkey, p_mfgr, p_size, p_type) values
    (1, 'MFGR#1', 25, 'SMALL TIN'),
    (2, 'MFGR#2', 26, 'SMALL TIN'),
    (3, 'MFGR#3', 25, 'SMALL BRASS');

insert into partsupp (ps_partkey, ps_suppkey, ps_supplycost) values
    (1, 100, 10.00),
    (1, 101, 20.00),
    (1, 200, 1.00),
    (2, 101, 5.00),
    (3, 100, 3.00);
