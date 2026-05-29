CREATE TABLE Users (
  Id INT,
  DisplayName STRING,
  Reputation INT,
  Views INT
);
CREATE TABLE Posts (
  Id INT,
  OwnerUserId INT,
  PostTypeId INT,
  Title STRING,
  CreationDate STRING
);
CREATE TABLE Votes (
  Id INT,
  PostId INT,
  VoteTypeId INT
);
