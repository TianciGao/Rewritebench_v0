CREATE TABLE Users (
  Id INT,
  DisplayName STRING,
  Reputation INT
);
CREATE TABLE Posts (
  Id INT,
  Title STRING,
  OwnerUserId INT,
  CreationDate STRING,
  Score INT,
  PostTypeId INT,
  Body STRING
);
CREATE TABLE Votes (
  Id INT,
  UserId INT,
  VoteTypeId INT,
  BountyAmount INT
);
CREATE TABLE Badges (
  Id INT,
  UserId INT,
  Class INT
);
