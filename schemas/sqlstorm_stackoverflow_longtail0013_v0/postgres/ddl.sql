CREATE TABLE Users (
  Id INT,
  DisplayName TEXT,
  Reputation INT
);
CREATE TABLE Posts (
  Id INT,
  Title TEXT,
  OwnerUserId INT,
  CreationDate TEXT,
  Score INT,
  PostTypeId INT,
  Body TEXT
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
