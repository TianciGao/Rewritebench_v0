-- PERF_0075 draft MySQL witness data for package enablement review only.
-- Derived mechanically from validation/pg_witness_data.sql.
-- Draft only: do not treat as executed or validated.

insert into date_dim values (1, 2002);

insert into customer_address values (10, 'IL');
insert into customer_address values (11, 'IL');

insert into customer values
  (100, 10, 'C100', 'Ms.', 'Ada', 'Lane', 'Y', 1, 1, 1980, 'US', 'ada', 'ada@example.com', 9001),
  (101, 11, 'C101', 'Mr.', 'Ben', 'Stone', 'N', 2, 2, 1981, 'US', 'ben', 'ben@example.com', 9002);

insert into web_returns values (100, 1, 10, 30.00);
insert into web_returns values (100, 1, 10, 6.00);
insert into web_returns values (101, 1, 11, 10.00);
