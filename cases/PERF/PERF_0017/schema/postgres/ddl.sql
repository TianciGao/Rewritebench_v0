-- PERF_0017 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table customer
(
    c_custkey integer not null,
    c_name varchar(25),
    c_address varchar(40),
    c_nationkey integer,
    c_phone varchar(15),
    c_acctbal numeric(15,2),
    c_comment varchar(117),
    primary key (c_custkey)
);

create table orders
(
    o_orderkey integer not null,
    o_custkey integer,
    o_orderdate date,
    primary key (o_orderkey)
);

create table lineitem
(
    l_orderkey integer,
    l_extendedprice numeric(15,2),
    l_discount numeric(15,2),
    l_returnflag char(1)
);

create table nation
(
    n_nationkey integer not null,
    n_name varchar(25),
    primary key (n_nationkey)
);
