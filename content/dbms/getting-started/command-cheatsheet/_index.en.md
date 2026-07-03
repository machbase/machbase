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

## Cheatsheet Verification Sample

```sql
CREATE TABLE DBMS_GS_CHEATSHEET (
  ID INTEGER,
  MESSAGE VARCHAR(40)
);

INSERT INTO DBMS_GS_CHEATSHEET VALUES (1, 'hello machbase');

SELECT ID, MESSAGE FROM DBMS_GS_CHEATSHEET;

DROP TABLE DBMS_GS_CHEATSHEET;
```

Assuming the SQL above is saved as `/tmp/dbms_gs_cheatsheet.sql`, run the following command.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_cheatsheet.sql
```

If `hello machbase` is printed, the basic command combination in the cheatsheet works.
If a rerun fails because `DBMS_GS_CHEATSHEET` already exists, run
`DROP TABLE DBMS_GS_CHEATSHEET;` and start again.
