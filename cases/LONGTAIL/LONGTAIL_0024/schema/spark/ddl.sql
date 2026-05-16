CREATE TABLE Posts (
  Id INT,
  Title STRING,
  Score INT,
  ViewCount INT
);

CREATE TABLE PostHistory (
  Id INT,
  PostId INT,
  UserId INT,
  PostHistoryTypeId INT,
  CreationDate TIMESTAMP,
  Text STRING
);
