CREATE TABLE Users (
  Id INT,
  DisplayName TEXT
);

CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  Title TEXT,
  Score INT
);

CREATE TABLE Comments (
  Id INT,
  PostId INT,
  UserId INT,
  Score INT,
  Text TEXT,
  CreationDate TIMESTAMP
);
