---
type: docs
title: 'First Steps with machsql'
weight: 20
toc: true
---

`machsql` is the command-line client used to send SQL to Machbase DBMS. You can run it
interactively or execute a SQL file with `-f`. This manual verifies samples with SQL
files because they are easy to repeat.

## Common Options

| Option | Meaning |
| --- | --- |
| `-s 127.0.0.1` | Server address |
| `-P 5656` | Server port |
| `-u SYS` | User name |
| `-p MANAGER` | Password |
| `-f file.sql` | SQL file to execute |

## machsql Sample

```sql
SHOW TABLES;
```

Assuming the SQL above is saved as `/tmp/dbms_gs_machsql.sql`, run the following command.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_machsql.sql
```

The `TABLE_TYPE` column shows which table types currently exist in the database.
