---
type: docs
title: 'SERIES BY'
weight: 90
toc: true
---

`SERIES BY`句はソート済みの結果集合から、特定条件を満たす連続した行の区間（series）を抽出します。連続区間の開始/終了時刻やパターンの分析に使用します。

## 構文

```sql
SELECT ...
  FROM table_name
 [WHERE ...]
 ORDER BY col [ASC | DESC]
 SERIES BY condition_expr
```

- `ORDER BY`句がなければ、`_ARRIVAL_TIME`列でソートします。
- `GROUP BY`を使用する場合や、`_ARRIVAL_TIME`列がないVOLATILE / LOOKUPテーブルでは、必ず`ORDER BY`を明示してください。
- `SERIES BY`条件を連続して満たす同一区間の行は、同じ`SERIESNUM()`値を持ちます。

## 例

### 基本的な使用方法

```sql
CREATE LOG TABLE t1 (c1 INTEGER, c2 INTEGER);
INSERT INTO t1 VALUES (0, 1);
INSERT INTO t1 VALUES (1, 2);
INSERT INTO t1 VALUES (2, 3);
INSERT INTO t1 VALUES (3, 2);
INSERT INTO t1 VALUES (4, 1);
INSERT INTO t1 VALUES (5, 2);
INSERT INTO t1 VALUES (6, 3);
INSERT INTO t1 VALUES (7, 1);

SELECT c1, c2
  FROM t1
 ORDER BY c1
 SERIES BY c2 > 1;
```

結果:

```
C1          C2
---------------------------
1           2
2           3
3           2
5           2
6           3
```

### SERIESNUM()で区間番号を確認

```sql
SELECT c1, c2, SERIESNUM() AS grp
  FROM t1
 ORDER BY c1
 SERIES BY c2 > 1;
```

結果:

```
C1          C2          GRP
-----------------------------------
1           2           1
2           3           1
3           2           1
5           2           2
6           3           2
```

### TAGテーブルで連続区間を分析

内側のクエリで連続区間別の番号を生成し、外側のクエリで区間番号を基準に集計します。

```sql
-- 100を超える連続区間ごとの開始/終了時刻と最大値を参照
SELECT MIN(time) AS start_time,
       MAX(time) AS end_time,
       MAX(value) AS peak_value,
       series_id
  FROM (
      SELECT time, value, SERIESNUM() AS series_id
        FROM tag
       WHERE name = 'PRESSURE-01'
         AND time >= TO_DATE('2024-01-01', 'YYYY-MM-DD')
       ORDER BY time
       SERIES BY value > 100.0
  )
 GROUP BY series_id
 ORDER BY series_id;
```

## 関連ドキュメント

- [SELECT hint syntax](../select-hint-syntax/) — SELECTヒントの構文と使用例
- [window function / OVER syntax](../window-function-over-syntax/) — ウィンドウを使った分析との違い
