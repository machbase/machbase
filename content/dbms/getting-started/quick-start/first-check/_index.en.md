---
type: docs
title: 'First Check After Installation'
weight: 10
toc: true
---

The first check is whether the DBMS server responds on port 5656 and whether `machsql`
can connect to it.

## Connection Command

For an interactive session, run `machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER` in a
terminal.

Use `-f` to run a SQL file. Every sample in this chapter is verified with that pattern.

## Server Check Sample

```sql
SELECT COUNT(*) AS TABLE_COUNT FROM M$SYS_TABLES;
```

Assuming the SQL above is saved as `/tmp/dbms_gs_first_check.sql`, run the following command.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_first_check.sql
```

On a successful connection, the `Machbase Client Query Utility` banner is followed by
the `TABLE_COUNT` result. If the connection fails, check the server address, port,
user name, and password first.
