-- PERF_0028 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.

create table orders
(
    o_orderkey integer not null,
    o_orderpriority varchar(20),
    primary key (o_orderkey)
);

create table lineitem
(
    l_orderkey integer,
    l_shipmode varchar(20),
    l_commitdate date,
    l_receiptdate date,
    l_shipdate date
);
