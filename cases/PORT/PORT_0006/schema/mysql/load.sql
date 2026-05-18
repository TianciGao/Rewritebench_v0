-- DRAFT witness fixture for PORT_0006; not validated evidence by itself
DROP TABLE IF EXISTS loan;

CREATE TABLE loan (
  status TEXT,
  account_id INT,
  amount DOUBLE -- conservative numeric choice; exact source type may differ
);

INSERT INTO loan (status, account_id, amount) VALUES
  ('C', 1, 90000),
  ('A', 2, 95000),
  ('C', 3, 100000),
  (NULL, 4, 87000);
