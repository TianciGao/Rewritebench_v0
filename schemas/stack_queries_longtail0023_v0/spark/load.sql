INSERT INTO Posts VALUES
  (201, 'Disk cleanup tips'),
  (202, 'Network latency issue'),
  (203, 'Printer setup help'),
  (204, 'Backup strategy'),
  (205, 'Isolated post'),
  (206, 'Mirror topic');

INSERT INTO PostLinks VALUES
  (1, 201, 202, 1, TIMESTAMP '2020-02-01 09:00:00'),
  (2, 201, 203, 1, TIMESTAMP '2020-02-01 09:05:00'),
  (3, 202, 201, 3, TIMESTAMP '2020-02-01 09:10:00'),
  (4, 202, 204, 1, TIMESTAMP '2020-02-01 09:15:00'),
  (5, 203, 201, 1, TIMESTAMP '2020-02-01 09:20:00'),
  (6, 204, 202, 1, TIMESTAMP '2020-02-01 09:25:00'),
  (7, 206, 201, 1, TIMESTAMP '2020-02-01 09:30:00');
