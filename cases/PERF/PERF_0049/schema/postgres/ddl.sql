create table store_sales (
    ss_sold_date_sk integer,
    ss_store_sk integer,
    ss_item_sk integer,
    ss_promo_sk integer,
    ss_ticket_number integer,
    ss_ext_sales_price decimal(9,2),
    ss_net_profit decimal(9,2)
);

create table store_returns (
    sr_item_sk integer,
    sr_ticket_number integer,
    sr_return_amt decimal(9,2),
    sr_net_loss decimal(9,2)
);

create table catalog_sales (
    cs_sold_date_sk integer,
    cs_catalog_page_sk integer,
    cs_item_sk integer,
    cs_promo_sk integer,
    cs_order_number integer,
    cs_ext_sales_price decimal(9,2),
    cs_net_profit decimal(9,2)
);

create table catalog_returns (
    cr_item_sk integer,
    cr_order_number integer,
    cr_return_amount decimal(9,2),
    cr_net_loss decimal(9,2)
);

create table web_sales (
    ws_sold_date_sk integer,
    ws_web_site_sk integer,
    ws_item_sk integer,
    ws_promo_sk integer,
    ws_order_number integer,
    ws_ext_sales_price decimal(9,2),
    ws_net_profit decimal(9,2)
);

create table web_returns (
    wr_item_sk integer,
    wr_order_number integer,
    wr_return_amt decimal(9,2),
    wr_net_loss decimal(9,2)
);

create table date_dim (
    d_date_sk integer primary key,
    d_date date
);

create table store (
    s_store_sk integer primary key,
    s_store_id varchar(20)
);

create table catalog_page (
    cp_catalog_page_sk integer primary key,
    cp_catalog_page_id varchar(20)
);

create table web_site (
    web_site_sk integer primary key,
    web_site_id varchar(20)
);

create table item (
    i_item_sk integer primary key,
    i_current_price decimal(9,2)
);

create table promotion (
    p_promo_sk integer primary key,
    p_channel_tv varchar(1)
);
