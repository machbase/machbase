---
title: SQL
type: docs
weight: 22
---

Select "SQL" to open a new sql editor.

{{< figure src="/images/web-sql-pick.png" width="600" >}}

## SQL

### Create table

The page shows the SQL editor on left panel and result and logs are on the right panel.

Copy the below DDL statement and paste it to the editor.

```sql
CREATE TAG TABLE IF NOT EXISTS example (
  name varchar(100) primary key,
  time datetime basetime,
  value double summarized
);
```

Execute the statement by hit "Ctrl+Enter" or click ▶︎ icon on the top-left of the panel. Don't forget the semi-colon of the end of the statement.

{{< figure src="/images/web-cretable.png" >}}

### Insert Table

Execute the statement below to write a single record of data.

```sql
INSERT INTO example VALUES('my-car', now, 1.2345);
```

{{< figure src="/images/web-insert.png" >}}

### Select Table

Execute the select statement below, it will show the result on the right tabular panel.

```sql
SELECT time, value FROM example WHERE name = 'my-car';
```

{{< figure src="/images/web-select.png" >}}

### Chart Draw

Insert more records by executing insert statement repeatedly.

```sql
INSERT INTO example VALUES('my-car', now, 1.2345*1.1);
INSERT INTO example VALUES('my-car', now, 1.2345*1.2);
INSERT INTO example VALUES('my-car', now, 1.2345*1.3);
```

Then review the stored 'my-car' records.

```sql
SELECT time, value FROM example WHERE name = 'my-car';
```
{{< figure src="/images/web-select-multi.png" >}}

Click *CHART* tab from the right side pane. It will show a line chart with the query result.

{{< figure src="/images/web-select-chart.jpg" width="600" >}}

### Download CSV file

The full result of the query can be exported in a CSV file.

{{< figure src="./img/web-select-download.png" >}}

### Delete Table

Delete records with a *DELETE* statement.

```sql
DELETE FROM example WHERE name = 'my-car'
```

Or, remove the table if you want to create a fresh one.

```sql
DROP TABLE example;
```

## Non-SQL

### show tables

Simplified command that queries `M$SYS_TABLES` table.

```
show tables;
```

{{< figure src="./img/web-show-tables.png" >}}

### desc _table_name_

Describe table's columns and related index.

```
desc example;
```

{{< figure src="./img/web-desc-table.png" >}}

### show tags _table_name_

```
show tags example;
```

Query stored tags of the table, it works to TAG table only.

{{< figure src="./img/web-show-tags.png" >}}


## SQL Guide

The following section provides an overview of the core concepts and features of TAG tables.  
For comprehensive details and additional features, refer to the [DBMS References](https://docs.machbase.com/dbms/).

{{< children_toc />}}
