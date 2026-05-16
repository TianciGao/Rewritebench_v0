CREATE TABLE posts (id INT, answercount INT) USING PARQUET;
CREATE TABLE postlinks (id INT, postid INT, creationdate TIMESTAMP) USING PARQUET;
