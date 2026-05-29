insert into lineitem (
	l_returnflag,
	l_linestatus,
	l_quantity,
	l_extendedprice,
	l_discount,
	l_tax,
	l_shipdate
) values
	('A', 'F', 10.00, 100.00, 0.05, 0.08, date '1998-08-26'),
	('A', 'F', 20.00, 200.00, 0.10, 0.05, date '1998-08-27'),
	('N', 'O', 15.00, 150.00, 0.00, 0.07, date '1998-08-20'),
	('R', 'F', 50.00, 500.00, 0.02, 0.04, date '1998-08-28');
