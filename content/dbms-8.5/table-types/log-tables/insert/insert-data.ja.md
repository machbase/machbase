---
title : INSERT
type: docs
weight: 10
toc: true
---

他の商用 RDBMS と同様に、テーブルを作成してから INSERT INTO 文でデータを挿入します。

Machbase は、対話型クエリーツール machsql を提供しています。


## テーブルの作成 {#create-table}

```sql
CREATE TABLE table_name ( column1 datatype, column2 datatype, column3 datatype, .... );
```

```sql
CREATE TABLE sensor_data ( id VARCHAR(32), val DOUBLE );
```


## データの挿入 {#data-insertion}

```sql
INSERT INTO table_name VALUES (value1, value2, value3, ...);
```

```sql
INSERT INTO sensor_data VALUES('sensor1', 10.1);
INSERT INTO sensor_data VALUES('sensor2', 20.2);
INSERT INTO sensor_data VALUES('sensor3', 30.3);
```


## 挿入結果の確認 {#confirm-data-insertion}

```sql
SELECT column1, column2, ... FROM table_name;
```

```sql
SELECT * FROM sensor_data;
```


## 操作の全体例 {#entire-process}

machsql を使用する例を示します。

```sql
Mach> CREATE TABLE sensor_data (id VARCHAR(32), val DOUBLE);
 Created successfully.
Mach> INSERT INTO sensor_data VALUES('sensor1', 10.1);
 1 row(s) inserted.
Mach> INSERT INTO sensor_data VALUES('sensor2', 20.2);
 1 row(s) inserted.
Mach> INSERT INTO sensor_data VALUES('sensor3', 30.3);
 1 row(s) inserted.
Mach> SELECT * FROM sensor_data;
ID VAL
-----------------------------------------------------------------
sensor3 30.3
sensor2 20.2
sensor1 10.1
[3] row(s) selected.
```
