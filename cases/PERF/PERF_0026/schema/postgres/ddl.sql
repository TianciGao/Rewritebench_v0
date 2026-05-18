-- PERF_0026 minimal PostgreSQL schema for referenced columns only.

create table customer (
    c_custkey integer primary key,
    c_phone varchar(15),
    c_acctbal numeric(15, 2)
);

create table orders (
    o_custkey integer
);
