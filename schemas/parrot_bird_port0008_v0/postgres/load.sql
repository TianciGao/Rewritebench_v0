-- DRAFT witness data only; not executed in this task
INSERT INTO frpm (cdscode) VALUES
  ('CDS_A'),
  ('CDS_B');
INSERT INTO schools (cdscode, county, city, doc, opendate, soc, admemail1, admemail2) VALUES
  ('CDS_A', 'San Bernardino', 'San Bernardino', '54', DATE '2009-08-01', '62', 'alpha_admin1@example.org', 'alpha_admin2@example.org'),
  ('CDS_B', 'San Bernardino', 'San Bernardino', '54', DATE '2009-08-01', '63', 'beta_admin1@example.org', 'beta_admin2@example.org');
