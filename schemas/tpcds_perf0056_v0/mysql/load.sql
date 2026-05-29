-- PERF_0056 draft MySQL witness data for package enablement review only.
-- Derived mechanically from validation/pg_witness_data.sql.
-- Draft only: do not treat as executed or validated.

insert into date_dim values (1, 2000, 2, 1200);

insert into item values
  (10, 25.00, 'Books'),
  (11, 10.00, 'Books');

insert into customer_address values (1, 'TN');
insert into customer values (101, 1);
insert into store_sales values (101, 1, 10);
insert into customer_address values (2, 'TN');
insert into customer values (102, 2);
insert into store_sales values (102, 1, 10);
insert into customer_address values (3, 'TN');
insert into customer values (103, 3);
insert into store_sales values (103, 1, 10);
insert into customer_address values (4, 'TN');
insert into customer values (104, 4);
insert into store_sales values (104, 1, 10);
insert into customer_address values (5, 'TN');
insert into customer values (105, 5);
insert into store_sales values (105, 1, 10);
insert into customer_address values (6, 'TN');
insert into customer values (106, 6);
insert into store_sales values (106, 1, 10);
insert into customer_address values (7, 'TN');
insert into customer values (107, 7);
insert into store_sales values (107, 1, 10);
insert into customer_address values (8, 'TN');
insert into customer values (108, 8);
insert into store_sales values (108, 1, 10);
insert into customer_address values (9, 'TN');
insert into customer values (109, 9);
insert into store_sales values (109, 1, 10);
insert into customer_address values (10, 'TN');
insert into customer values (110, 10);
insert into store_sales values (110, 1, 10);
