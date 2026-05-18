-- PERF_0073 minimal Spark SQL schema for referenced columns only.

create table store_sales (
  ss_quantity int,
  ss_list_price decimal(12, 2),
  ss_coupon_amt decimal(12, 2),
  ss_wholesale_cost decimal(12, 2)
);
