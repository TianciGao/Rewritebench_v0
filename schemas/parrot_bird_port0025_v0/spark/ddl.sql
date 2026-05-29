CREATE TABLE account (account_id INT, account_date DATE) USING PARQUET;
CREATE TABLE loan (account_id INT, duration INT, amount INT) USING PARQUET;
