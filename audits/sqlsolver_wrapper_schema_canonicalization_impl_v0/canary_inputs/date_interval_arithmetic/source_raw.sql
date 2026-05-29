SELECT SUM(l_extendedprice) FROM lineitem WHERE l_shipdate < DATE '1995-01-01' + INTERVAL '1' YEAR;
