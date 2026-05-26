# Before/After `pos_01.sql` Diff

```diff
diff --git a/cases/LONGTAIL/LONGTAIL_0011/sql/pos_01.sql b/cases/LONGTAIL/LONGTAIL_0011/sql/pos_01.sql
index 7dc1884..9175a68 100644
--- a/cases/LONGTAIL/LONGTAIL_0011/sql/pos_01.sql
+++ b/cases/LONGTAIL/LONGTAIL_0011/sql/pos_01.sql
@@ -6,11 +6,22 @@ WITH RankedPosts AS (
         p.Score,
         p.ViewCount,
         u.DisplayName AS OwnerDisplayName,
-        DENSE_RANK() OVER (PARTITION BY p.OwnerUserId ORDER BY p.Score ASC) AS WorstRank
+        DENSE_RANK() OVER (
+            PARTITION BY p.OwnerUserId
+            ORDER BY p.Score DESC
+        ) AS PostRank
     FROM Posts p
-    JOIN Users u ON p.OwnerUserId = u.Id
+    JOIN Users u
+      ON p.OwnerUserId = u.Id
     WHERE p.PostTypeId = 1
       AND p.CreationDate >= '2022-01-01'
+),
+MaxRank AS (
+    SELECT
+        OwnerDisplayName,
+        MAX(PostRank) AS MaxPostRank
+    FROM RankedPosts
+    GROUP BY OwnerDisplayName
 )
 SELECT
     rp.Title,
@@ -19,5 +30,7 @@ SELECT
     rp.ViewCount,
     rp.OwnerDisplayName
 FROM RankedPosts rp
-WHERE rp.WorstRank = 1
+JOIN MaxRank mr
+  ON rp.OwnerDisplayName = mr.OwnerDisplayName
+WHERE rp.PostRank = mr.MaxPostRank
 ORDER BY rp.Score DESC, rp.ViewCount DESC;
```
