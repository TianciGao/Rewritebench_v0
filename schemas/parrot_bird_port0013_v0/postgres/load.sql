-- DRAFT witness data only; not executed in this task
INSERT INTO district (district_id, a11) VALUES
  (1, 20000.0),
  (2, 9000.0);
INSERT INTO client (client_id, district_id, gender) VALUES
  (11, 1, 'F'),
  (12, 1, 'F'),
  (13, 1, 'M'),
  (21, 2, 'M');
