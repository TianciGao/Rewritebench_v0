create table lineitem (
	l_returnflag char(1) not null,
	l_linestatus char(1) not null,
	l_quantity numeric(15, 2) not null,
	l_extendedprice numeric(15, 2) not null,
	l_discount numeric(15, 2) not null,
	l_tax numeric(15, 2) not null,
	l_shipdate date not null
);
