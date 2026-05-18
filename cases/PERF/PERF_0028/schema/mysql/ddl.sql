-- PERF_0028 minimal MySQL schema for referenced columns only.

create table orders (
    o_orderkey integer primary key,
    o_orderpriority varchar(20)
);

create table lineitem (
    l_orderkey integer,
    l_shipmode varchar(20),
    l_commitdate date,
    l_receiptdate date,
    l_shipdate date
);
