---
type: docs
title: 'Basic Command Cheatsheet'
weight: 30
toc: true
---

You do not need many commands at the beginning. The commands below are enough to
connect, inspect tables, and repeat the first SQL workflow.

| Task | Command |
| --- | --- |
| Interactive connection | `machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER` |
| Run a SQL file | `machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f file.sql` |
| List tables | `SHOW TABLES;` |
| Create a table | `CREATE TABLE table_name (...);` |
| Insert data | `INSERT INTO table_name VALUES (...);` |
| Query data | `SELECT ... FROM table_name;` |
| Drop a table | `DROP TABLE table_name;` |

The representative sample combines these commands once. This cheatsheet does not add
another verification procedure; use it to remember each command's role.
