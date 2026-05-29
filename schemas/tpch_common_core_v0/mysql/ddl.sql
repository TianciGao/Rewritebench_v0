create table lineitem (
	l_returnflag char(1) not null,
	l_linestatus char(1) not null,
	l_quantity decimal(15, 2) not null,
	l_extendedprice decimal(15, 2) not null,
	l_discount decimal(15, 2) not null,
	l_tax decimal(15, 2) not null,
	l_shipdate date not null
);
