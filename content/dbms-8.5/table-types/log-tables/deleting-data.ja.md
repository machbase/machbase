---
title : Log データの削除
type: docs
weight: 40
toc: true
---

Machbase では、DELETE 文を Log テーブルに対して実行できます。

途中の任意のレコードだけを削除することはできません。指定した位置から最も古いレコードまでを連続して削除します。これはログデータの特性に基づく方式で、記録済みファイルを削除して空き領域を確保する操作に相当します。

次の形式を使用できます。

##  構文 {#syntax}

```sql
DELETE FROM table_name;
DELETE FROM table_name OLDEST number ROWS;
DELETE FROM table_name EXCEPT number ROWS;
DELETE FROM table_name EXCEPT number [YEAR | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND];
DELETE FROM table_name BEFORE datetime_expr;
```


##  例 {#example}

各例は、異なる初期データ状態で個別に実行したものです。

```sql
-- すべてのデータを削除する。
mach>DELETE FROM devices;
10 row(s) deleted.
 
-- 最も古い 5 件を削除する。
mach>DELETE FROM devices OLDEST 5 ROWS;
5 row(s) deleted.
 
-- 最新の 5 件を残して削除する。
mach>DELETE FROM devices EXCEPT 5 ROWS;
15 row(s) deleted.
 
-- 2018 年 6 月 1 日以前のデータを削除する。
mach>DELETE FROM devices BEFORE TO_DATE('2018-06-01', 'YYYY-MM-DD');
50 row(s) deleted.
```
