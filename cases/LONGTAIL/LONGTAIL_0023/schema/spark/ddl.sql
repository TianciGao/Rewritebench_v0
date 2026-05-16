CREATE TABLE Posts (
  Id INT,
  Title STRING
);

CREATE TABLE PostLinks (
  Id INT,
  PostId INT,
  RelatedPostId INT,
  LinkTypeId INT,
  CreationDate TIMESTAMP
);
