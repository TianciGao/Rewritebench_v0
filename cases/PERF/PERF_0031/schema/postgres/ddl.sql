-- PERF_0031 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.

create table supplier
(
    s_suppkey integer not null,
    s_name varchar(100),
    s_address varchar(200),
    s_phone varchar(40),
    primary key (s_suppkey)
);

create table lineitem
(
    l_suppkey integer,
    l_extendedprice numeric(12, 2),
    l_discount numeric(12, 2),
    l_shipdate date
);
