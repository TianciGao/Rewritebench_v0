INSERT INTO Users VALUES
  (1, 'Alice'),
  (2, 'Bob'),
  (3, 'Cara'),
  (4, 'Dan');

INSERT INTO Posts VALUES
  (101, 1, 'Disk cleanup tips', 10),
  (102, 2, 'Network latency issue', 8),
  (103, 3, 'Printer setup help', 5),
  (104, 4, 'Backup strategy', 7),
  (105, 2, 'Isolated note', 1);

INSERT INTO Comments VALUES
  (1, 101, 2, 2, 'try cleanup tool', '2020-01-01 10:00:00'),
  (2, 101, 2, 1, 'check temp files', '2020-01-01 10:05:00'),
  (3, 101, 3, 3, 'review logs', '2020-01-01 10:10:00'),
  (4, 101, 4, 1, 'monitor free space', '2020-01-01 10:15:00'),
  (5, 102, 1, 1, 'measure packet loss', '2020-01-02 09:00:00'),
  (6, 102, 3, 2, 'replace cable', '2020-01-02 09:05:00'),
  (7, 102, 3, 1, 'check router', '2020-01-02 09:06:00'),
  (8, 103, 2, 1, 'driver reinstall', '2020-01-03 08:00:00'),
  (9, 104, 1, 2, 'use snapshots', '2020-01-04 07:00:00'),
  (10, 104, 2, 1, 'verify restore path', '2020-01-04 07:05:00'),
  (11, 104, 3, 1, 'test recovery', '2020-01-04 07:10:00'),
  (12, 105, 4, 1, 'single comment', '2020-01-05 11:00:00');
