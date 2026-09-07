---
type: docs
title: '1.3 Basic Command Cheatsheet'
weight: 30
toc: true
---

Run connection commands in your operating system's terminal and SQL in a connected `machsql`
session. Adjust the server address, port, and account for your environment. `MANAGER` in these
examples is the initial practice password used in the quick start. If it has been changed, use
the account's current password.

## Commands to Run in the Terminal

| Task | Command |
|---|---|
| Connect interactively | `machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER` |
| Run a SQL file | `machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f file.sql` |

## SQL to Run in machsql

| Task | Command |
|---|---|
| List tables | `SHOW TABLES;` |
| Inspect columns and types | `DESC table_name;` |
| Create a TRANSACTION table | `CREATE TRANSACTION TABLE table_name (...);` |
| Create a LOG table | `CREATE LOG TABLE table_name (...);` |
| Insert data | `INSERT INTO table_name VALUES (...);` |
| Query matching data | `SELECT ... FROM table_name WHERE ...;` |
| Sort query results | `SELECT ... FROM table_name ORDER BY ...;` |
| Delete a table and its data | `DROP TABLE table_name;` |

`table_name` and `...` are placeholders that must be replaced with actual names and definitions.
For runnable SQL, use [Quick Start](../quick-start/).
`DROP TABLE` also deletes the table's data, so first confirm that it is the practice table you
intend to remove.

In Machbase DBMS 8.7.0, `CREATE TABLE` without a table type creates a TRANSACTION table.
TRANSACTION tables are supported in Standard Edition. Specifying the type makes the intent of
an example clear. For the complete command reference, see
[machsql](../../reference/command-line-tools/dictionary-machsql/).
