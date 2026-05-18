insert into date_dim values (1, '1998Q1');
insert into date_dim values (2, '1998Q2');
insert into date_dim values (3, '1998Q3');
insert into store values (10, 'TN');
insert into item values (20, 'ITEM-20', 'Witness item');
insert into store_sales values (1, 20, 10, 100, 5000, 4);
insert into store_returns values (100, 20, 5000, 2, 1);
insert into catalog_sales values (100, 20, 3, 7);
