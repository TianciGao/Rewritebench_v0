-- PERF_0031 minimal Spark SQL schema for referenced columns only.

create table supplier (
    s_suppkey int,
    s_name string,
    s_address string,
    s_phone string
);

create table lineitem (
    l_suppkey int,
    l_extendedprice decimal(12, 2),
    l_discount decimal(12, 2),
    l_shipdate date
);
