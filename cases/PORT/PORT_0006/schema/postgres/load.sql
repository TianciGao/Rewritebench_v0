-- DRAFT witness load for PORT_0006; not executed in this task
TRUNCATE TABLE loan;

INSERT INTO loan (status, account_id, amount) VALUES
  ('C', 1, 90000),
  ('A', 2, 95000),
  ('C', 3, 100000),
  (NULL, 4, 87000);
