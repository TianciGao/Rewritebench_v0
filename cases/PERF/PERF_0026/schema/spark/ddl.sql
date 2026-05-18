-- PERF_0026 minimal Spark SQL schema for referenced columns only.

create table customer (
    c_custkey int,
    c_phone string,
    c_acctbal decimal(15, 2)
);

create table orders (
    o_custkey int
);
