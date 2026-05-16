SELECT 1.0 * COUNT(t1.id) / 12 FROM postlinks AS t1 INNER JOIN posts AS t2 ON t1.postid = t2.id WHERE t2.answercount <= 2 AND EXTRACT(YEAR FROM CAST(t1.creationdate AS TIMESTAMP)) = 2010
