-- PERF_0028 minimal Spark SQL schema for referenced columns only.

create table orders (
    o_orderkey int,
    o_orderpriority string
);

create table lineitem (
    l_orderkey int,
    l_shipmode string,
    l_commitdate date,
    l_receiptdate date,
    l_shipdate date
);
