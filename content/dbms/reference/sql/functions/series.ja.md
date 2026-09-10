---
type: docs
title: 'ウィンドウ/系列関数'
weight: 20
toc: true
---

このページでは、結果行に番号を付ける`ROWNUM()`と連続区間を区別する`SERIESNUM()`を説明します。
`SERIES BY`は、ソート済みデータ内で条件を連続して満たす区間の分析に使用します。
`LAG()`や`LEAD()`など`OVER`句を使用する関数は、
[ウィンドウ関数構文](../../syntax/window-function-over-syntax/)を参照してください。

## クイックリファレンス

| 関数 | 構文 | 説明 |
|------|------|------|
| ROWNUM | `ROWNUM()` | SELECT結果の行番号を付与 |
| SERIESNUM | `SERIESNUM()` | 行が属する連続区間の番号（同じ区間の行は同じ番号） |

---

## ROWNUM

`SELECT`の結果行に連番を付けます。サブクエリやインラインビュー内でも使用できます。インラインビューの選択リストで使用する場合は、外部から参照できるように別名を指定してください。

```sql
ROWNUM()
```

### 使用できる句

| 使用可能 | 使用不可 |
|-----------|----------|
| SELECT Target List, GROUP BY, ORDER BY | WHERE, HAVING |

`WHERE` / `HAVING`で行番号を使って絞り込むには、インラインビューで`ROWNUM()`を計算し、外側のクエリから参照します。

```sql
-- 先頭2行のみ選択
Mach> SELECT INNER_RANK, c3 AS NAME
        FROM (SELECT ROWNUM() AS INNER_RANK, * FROM rownum_table)
       WHERE INNER_RANK < 3;
INNER_RANK           NAME
--------------------------
1                    Fourth Row
2                    Third Row
```

### ORDER BYとの併用

`ORDER BY`を含むクエリをインラインビューにし、外側の`SELECT`で`ROWNUM()`を呼び出すと、ソート順に番号が付きます。

```sql
Mach> SELECT ROWNUM(), c2 AS SORT, c3 AS NAME
        FROM (SELECT * FROM rownum_table ORDER BY c3);
ROWNUM()    SORT    NAME
--------------------------
1           1       NULL
2           2       John
3           4.3     Micheal
4           3.3     Sarah
```

---

## SERIESNUM

`SERIES BY`句でグループ化された系列で、各レコードが属する系列の番号を返します。`SERIES BY`句を使用しない場合は常に1を返します。戻り値の型は`BIGINT`です。

```sql
SERIESNUM()
```

```sql
Mach> CREATE LOG TABLE T1 (C1 INTEGER, C2 INTEGER);
Mach> INSERT INTO T1 VALUES (0, 1);
Mach> INSERT INTO T1 VALUES (1, 2);
Mach> INSERT INTO T1 VALUES (2, 3);
Mach> INSERT INTO T1 VALUES (3, 2);
Mach> INSERT INTO T1 VALUES (4, 1);
Mach> INSERT INTO T1 VALUES (5, 2);
Mach> INSERT INTO T1 VALUES (6, 3);
Mach> INSERT INTO T1 VALUES (7, 1);

-- C2 > 1を満たす連続区間を系列に分割
Mach> SELECT SERIESNUM(), C1, C2 FROM T1 ORDER BY C1 SERIES BY C2 > 1;
SERIESNUM()  C1  C2
--------------------
1            1   2
1            2   3
1            3   2
2            5   2
2            6   3
[5] row(s) selected.
```

- `C1=1,2,3`（C2>1を満たす連続区間）→ 系列1
- `C1=4`（C2=1、条件を満たさない）→ 系列の境界
- `C1=5,6`（C2>1を満たす連続区間）→ 系列2

---

## SERIES BY句の概要

`SERIES BY`句は`ORDER BY`と併用し、指定した条件を連続して満たす行を1つの系列にまとめます。`SERIESNUM()`で各系列を区別し、集約関数と組み合わせて連続区間別の統計を計算できます。

区間別統計は、内側のクエリで区間番号を生成し、外側のクエリで集計します。
次の例の`threshold`は、比較するしきい値に置き換えてください。

```sql
SELECT series_id, COUNT(*), AVG(value)
  FROM (
      SELECT value, SERIESNUM() AS series_id
        FROM sensor_log
       ORDER BY ts
       SERIES BY value > threshold
  )
 GROUP BY series_id
 ORDER BY series_id;
```
