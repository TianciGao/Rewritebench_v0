-- DRAFT witness fixture for PORT_0005; not validated evidence by itself
DROP TABLE IF EXISTS drivers;

CREATE TABLE drivers (
  nationality TEXT,
  dob DATETIME
);

INSERT INTO drivers (nationality, dob) VALUES
  ('argentina_null', NULL),
  ('japan_earliest', '1979-07-04 00:00:00'),
  ('canada_mid', '1985-02-11 00:00:00'),
  ('brazil_latest', '1992-09-30 00:00:00');
