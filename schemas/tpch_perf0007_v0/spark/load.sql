insert into lineitem (
	l_shipdate,
	l_discount,
	l_quantity,
	l_extendedprice
) values
	(date '1995-01-01', 0.09, 10.00, 100.00),
	(date '1995-06-15', 0.08, 24.00, 200.00),
	(date '1995-12-31', 0.10, 25.00, 300.00),
	(date '1996-01-01', 0.09, 5.00, 400.00),
	(date '1995-07-01', 0.11, 5.00, 500.00);
