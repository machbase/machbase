---
title: Web UI
type: docs
weith: 13
---

It provides a built-in web UI for easy handling of Machbase Neo.

Open http://127.0.0.1:5654/ with web browser. Enter ID/Password as 'sys' and 'manager' which is the default.

> If the machbase-neo process is running in a remote machine, please refer [Start and Stop](../start-stop), it shows how to make machbase-neo remote-accessible.

![web-login](/images/web-login.png)

## SQL

Select "SQL" to open a new sql editor.

![web-sql](/images/web-sql-pick.png)

### Create table

The page shows the SQL editor on left panel and result and logs are on the right panel.

Copy the below DDL statement and paste it to the editor.

```sql
CREATE TAG TABLE IF NOT EXISTS example (
  name varchar(100) primary key,
  time datetime basetime,
  value double
);
```

Execute the statement by hit "Ctrl+Enter" or click ▶︎ icon on the top-left of the panel. Don't forget the semi-colon of the end of the statement.

![web-cretate](/images/web-cretable.png)

### Insert Table

Execute the statement below to write a single record of data.

```sql
INSERT INTO example VALUES('my-car', now, 1.2345);
```

![web-insert](/images/web-insert.png)

### Select Table

Execute the select statement below, it will show the result on the right tabular panel.

```sql
SELECT time, value FROM example WHERE name = 'my-car';
```

![webui-select](/images/web-select.png)

### Chart Draw

Insert more records by executing insert statement repeately.

```sql
INSERT INTO example VALUES('my-car', now, 1.2345*1.1);
INSERT INTO example VALUES('my-car', now, 1.2345*1.2);
INSERT INTO example VALUES('my-car', now, 1.2345*1.3);
```

Then review the stored 'my-car' records.

```sql
SELECT time, value FROM example WHERE name = 'my-car';
```
![webui-select-multi](/images/web-select-multi.png)

Click *CHART* tab from the right side pane. It will show a line chart with the query result.

![webui-select-chart](/images/web-select-chart.jpg)

### Delete Table

Delete records with a *DELETE* statement.

```sql
DELETE FROM example WHERE name = 'my-car'
```

Or, remove the table if you want to create a fresh one.

```sql
DROP TABLE example;
```

## Shell

Click the Shell tab to run the interactive shell on the web.

![web-shell](/images/web-shell-pick.png)

![web-shell-ui](/images/web-shell-ui.png)
