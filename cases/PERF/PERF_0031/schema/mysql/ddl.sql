-- PERF_0031 minimal MySQL schema for referenced columns only.

create table supplier (
    s_suppkey integer primary key,
    s_name varchar(100),
    s_address varchar(200),
    s_phone varchar(40)
);

create table lineitem (
    l_suppkey integer,
    l_extendedprice decimal(12, 2),
    l_discount decimal(12, 2),
    l_shipdate date
);
