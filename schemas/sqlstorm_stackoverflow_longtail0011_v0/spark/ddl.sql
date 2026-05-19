CREATE TABLE Users (
  Id INT,
  DisplayName STRING
);
CREATE TABLE Posts (
  Id INT,
  Title STRING,
  CreationDate STRING,
  Score INT,
  ViewCount INT,
  OwnerUserId INT,
  PostTypeId INT
);
