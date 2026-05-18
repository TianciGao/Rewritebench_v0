-- PERF_0009 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table orders
(
    o_orderkey integer not null,
    o_orderpriority varchar(20),
    o_orderdate date,
    primary key (o_orderkey)
);

create table lineitem
(
    l_orderkey integer,
    l_commitdate date,
    l_receiptdate date
);
