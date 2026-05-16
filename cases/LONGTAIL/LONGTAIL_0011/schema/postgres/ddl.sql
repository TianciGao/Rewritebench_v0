CREATE TABLE Users (
  Id INT,
  DisplayName TEXT
);
CREATE TABLE Posts (
  Id INT,
  Title TEXT,
  CreationDate TEXT,
  Score INT,
  ViewCount INT,
  OwnerUserId INT,
  PostTypeId INT
);
