CREATE TABLE Posts (
  Id INT,
  Title TEXT,
  Score INT,
  ViewCount INT
);

CREATE TABLE PostHistory (
  Id INT,
  PostId INT,
  UserId INT,
  PostHistoryTypeId INT,
  CreationDate TIMESTAMP,
  Text TEXT
);
