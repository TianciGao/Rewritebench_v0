CREATE TABLE Users (
  Id INT,
  DisplayName TEXT,
  Reputation INT,
  Views INT
);
CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  PostTypeId INT,
  Title TEXT,
  CreationDate TEXT
);
CREATE TABLE Votes (
  Id INT,
  PostId INT,
  VoteTypeId INT
);
