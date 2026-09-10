---
type: docs
title : Log テーブルの作成と管理
weight: 10
toc: true
---

Log テーブルは次のように作成します。

sensor_data テーブルを作成し、削除する例を示します。

使用できるデータ型は、SQL リファレンスのデータ型を参照してください。


## Log テーブルの作成 {#creating-log-table}

`CREATE TABLE` 構文で Log テーブルを作成します。

```sql
Mach> CREATE TABLE sensor_data (id VARCHAR(32), val DOUBLE);
Created successfully.
 
Mach> DROP TABLE sensor_data;
Dropped successfully.
```


## Log テーブルの削除 {#deleting-log-table}

`DROP TABLE` 文で Log テーブルを削除します。以下の DROP と TRUNCATE は、それぞれテーブルが存在する状態で個別に実行する例です。

```sql
-- DROP はデータとテーブルの両方を削除する。
Mach> DROP TABLE sensor_data;
Dropped successfully.
 
-- TRUNCATE はデータのみを削除し、テーブルを残す。
Mach> TRUNCATE TABLE sensor_data;
Truncated successfully.
```
