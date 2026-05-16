CREATE TABLE Users (
  Id INT,
  DisplayName STRING
);

CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  Title STRING,
  Score INT
);

CREATE TABLE Comments (
  Id INT,
  PostId INT,
  UserId INT,
  Score INT,
  Text STRING,
  CreationDate TIMESTAMP
);
